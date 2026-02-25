#!/usr/bin/env python3
"""
Migration script to transfer jobs from SQLite to PostgreSQL.
Usage: python -m scripts.migrate_to_postgres
"""

from __future__ import annotations

import asyncio
import json
import sqlite3
from pathlib import Path
from typing import Any, Optional

import asyncpg


def read_from_sqlite(db_path: str) -> list[dict[str, Any]]:
    """Read all jobs from SQLite database."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs")
    rows = cursor.fetchall()
    jobs = []

    for row in rows:
        job = dict(row)
        for key, value in job.items():
            if key in ("tech_stack", "attachments") and value is not None:
                try:
                    job[key] = json.dumps(json.loads(value))
                except (json.JSONDecodeError, TypeError):
                    job[key] = value
        jobs.append(job)

    conn.close()
    return jobs


async def ensure_table_exists(database_url: str) -> None:
    """Create jobs table if it doesn't exist (PostgreSQL-specific)."""
    db_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
    conn: asyncpg.Connection = await asyncpg.connect(db_url)

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id SERIAL PRIMARY KEY,
            title VARCHAR NOT NULL,
            company VARCHAR NOT NULL,
            url VARCHAR,
            date_applied VARCHAR NOT NULL,
            status VARCHAR NOT NULL,
            work_model VARCHAR,
            salary_range VARCHAR,
            salary_frequency VARCHAR DEFAULT 'Yearly',
            tech_stack TEXT,
            notes TEXT,
            screenshot_url VARCHAR,
            resume_url VARCHAR,
            cover_letter_url VARCHAR,
            attachments TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    """)
    await conn.close()


async def export_to_json(jobs: list[dict[str, Any]], output_path: str) -> None:
    """Export jobs to JSON file for backup."""
    with open(output_path, "w") as f:
        json.dump(jobs, f, indent=2, default=str)
    print(f"      Exported {len(jobs)} jobs to {output_path}")


async def insert_into_postgres(jobs: list[dict[str, Any]], database_url: str) -> int:
    """Insert jobs into PostgreSQL database."""
    db_url = database_url.replace("postgresql+asyncpg://", "postgresql://")

    conn: asyncpg.Connection = await asyncpg.connect(db_url)

    inserted = 0
    for job in jobs:
        values = {
            "id": job.get("id"),
            "title": job.get("title"),
            "company": job.get("company"),
            "url": job.get("url"),
            "date_applied": job.get("date_applied"),
            "status": job.get("status"),
            "work_model": job.get("work_model"),
            "salary_range": job.get("salary_range"),
            "salary_frequency": job.get("salary_frequency", "Yearly"),
            "tech_stack": job.get("tech_stack"),
            "notes": job.get("notes"),
            "screenshot_url": job.get("screenshot_url"),
            "resume_url": job.get("resume_url"),
            "cover_letter_url": job.get("cover_letter_url"),
            "attachments": job.get("attachments"),
            "created_at": job.get("created_at"),
            "updated_at": job.get("updated_at"),
        }

        null_fields = [k for k, v in values.items() if v is None]
        for field in null_fields:
            values[field] = None

        columns = ", ".join(values.keys())
        placeholders = ", ".join([f"${i + 1}" for i in range(len(values))])

        query = f"""
            INSERT INTO jobs ({columns})
            VALUES ({placeholders})
            ON CONFLICT (id) DO UPDATE SET
                title = EXCLUDED.title,
                company = EXCLUDED.company,
                url = EXCLUDED.url,
                date_applied = EXCLUDED.date_applied,
                status = EXCLUDED.status,
                work_model = EXCLUDED.work_model,
                salary_range = EXCLUDED.salary_range,
                salary_frequency = EXCLUDED.salary_frequency,
                tech_stack = EXCLUDED.tech_stack,
                notes = EXCLUDED.notes,
                screenshot_url = EXCLUDED.screenshot_url,
                resume_url = EXCLUDED.resume_url,
                cover_letter_url = EXCLUDED.cover_letter_url,
                attachments = EXCLUDED.attachments,
                updated_at = EXCLUDED.updated_at
        """

        await conn.execute(query, *list(values.values()))
        inserted += 1

    await conn.close()
    return inserted


async def verify_counts(sqlite_count: int, database_url: str) -> tuple[int, int]:
    """Verify row counts match between SQLite and PostgreSQL."""
    db_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
    conn: asyncpg.Connection = await asyncpg.connect(db_url)

    postgres_count = await conn.fetchval("SELECT COUNT(*) FROM jobs")

    await conn.close()

    return sqlite_count, postgres_count


async def main():
    """Main migration function."""
    import os

    sqlite_path = "../job-tracker/jobs.db"
    # Use DATABASE_URL from environment - required for security
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise ValueError(
            "DATABASE_URL environment variable is required. "
            "Run: export DATABASE_URL='postgresql+asyncpg://...'"
        )

    print("=" * 60)
    print("SQLite to PostgreSQL Migration")
    print("=" * 60)

    # Step 0: Ensure PostgreSQL table exists
    print("\n[0/5] Ensuring PostgreSQL table exists...")
    await ensure_table_exists(database_url)
    print("      Table ready")

    # Step 1: Read from SQLite and export to JSON
    print("\n[1/5] Reading jobs from SQLite...")
    jobs = read_from_sqlite(sqlite_path)
    sqlite_count = len(jobs)
    print(f"      Found {sqlite_count} jobs in SQLite")

    if sqlite_count > 0:
        await export_to_json(jobs, "jobs_export.json")

    if sqlite_count == 0:
        print("      No data to migrate.")
    else:
        # Step 2: Insert into PostgreSQL
        print("\n[2/5] Inserting jobs into PostgreSQL...")
        inserted = await insert_into_postgres(jobs, database_url)
        print(f"      Inserted {inserted} jobs")

    # Step 3: Verify counts
    print("\n[3/5] Verifying record counts...")
    sqlite_ct, postgres_ct = await verify_counts(sqlite_count, database_url)
    print(f"      SQLite count:  {sqlite_ct}")
    print(f"      PostgreSQL count: {postgres_ct}")

    # Step 4: Verify JSON fields
    print("\n[4/5] Verifying JSON fields...")
    db_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
    conn: asyncpg.Connection = await asyncpg.connect(db_url)

    if sqlite_count > 0:
        test_job = await conn.fetchrow(
            "SELECT tech_stack, attachments FROM jobs LIMIT 1"
        )
        print(f"      Sample tech_stack: {test_job['tech_stack']}")
        print(f"      Sample attachments: {test_job['attachments']}")

    await conn.close()

    print("\n[5/5] Migration complete!")

    print("\n" + "=" * 60)
    if sqlite_ct == postgres_ct:
        print("SUCCESS: Row counts match!")
    else:
        print(f"WARNING: Mismatch! SQLite={sqlite_ct}, PostgreSQL={postgres_ct}")
    print("=" * 60)

    return sqlite_ct == postgres_ct


if __name__ == "__main__":
    asyncio.run(main())
