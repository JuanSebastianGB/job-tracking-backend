import json
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse, JobUpdate


def _parse_json_field(value: any) -> any:
    """Parse JSON field - handles both string and already-parsed values."""
    if value is None:
        return None
    if isinstance(value, str):
        return json.loads(value)
    return value


def _job_to_response(job: Job) -> JobResponse:
    # Parse JSONB fields (can be strings or Python objects depending on SQLAlchemy version)
    tech_stack = _parse_json_field(job.tech_stack) or []
    attachments = _parse_json_field(job.attachments) or []

    job_dict = {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "url": job.url,
        "date_applied": job.date_applied,
        "status": job.status,
        "work_model": job.work_model,
        "salary_range": job.salary_range,
        "salary_frequency": job.salary_frequency,
        "tech_stack": tech_stack,
        "notes": job.notes,
        "screenshot_url": job.screenshot_url,
        "resume_url": job.resume_url,
        "cover_letter_url": job.cover_letter_url,
        "attachments": attachments,
        "created_at": job.created_at,
        "updated_at": job.updated_at,
    }
    return JobResponse(**job_dict)


async def create_job(db: AsyncSession, job: JobCreate) -> JobResponse:
    job_dict = job.model_dump()
    # With JSONB, pass Python objects directly (no serialization needed)
    # SQLAlchemy handles the conversion to JSONB automatically

    db_job = Job(**job_dict)
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)

    return _job_to_response(db_job)


async def get_jobs(db: AsyncSession) -> List[JobResponse]:
    result = await db.execute(select(Job).order_by(Job.date_applied.desc()))
    jobs = result.scalars().all()

    return [_job_to_response(job) for job in jobs]


async def get_job(db: AsyncSession, job_id: int) -> Optional[JobResponse]:
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()

    if job is None:
        return None

    return _job_to_response(job)


async def update_job(
    db: AsyncSession, job_id: int, job: JobUpdate
) -> Optional[JobResponse]:
    result = await db.execute(select(Job).where(Job.id == job_id))
    db_job = result.scalar_one_or_none()

    if db_job is None:
        return None

    update_data = job.model_dump(exclude_unset=True)
    # With JSONB, pass Python objects directly (no serialization needed)

    for field, value in update_data.items():
        setattr(db_job, field, value)

    await db.commit()
    await db.refresh(db_job)

    return _job_to_response(db_job)


async def delete_job(db: AsyncSession, job_id: int) -> bool:
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()

    if job is None:
        return False

    await db.delete(job)
    await db.commit()

    return True
