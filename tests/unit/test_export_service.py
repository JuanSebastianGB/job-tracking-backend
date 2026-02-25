"""Unit tests for export_service: generate_csv (4.2) and generate_json (4.3)."""
import csv
import json

import pytest

from app.schemas.job import JobResponse
from app.services.export_service import generate_csv, generate_json


# --- 4.2 generate_csv ---

EXPECTED_CSV_HEADERS = [
    "id",
    "title",
    "company",
    "url",
    "date_applied",
    "status",
    "work_model",
    "salary_range",
    "salary_frequency",
    "tech_stack",
    "notes",
    "screenshot_url",
    "resume_url",
    "cover_letter_url",
    "attachments",
    "created_at",
    "updated_at",
]


def test_generate_csv_headers_row_present_and_correct(sample_job_response):
    """CSV has a header row with all expected job field names."""
    jobs = [sample_job_response]
    content = generate_csv(jobs)
    lines = content.strip().split("\n")
    assert len(lines) >= 1
    first_row = next(csv.reader([lines[0]]))
    assert first_row == EXPECTED_CSV_HEADERS


def test_generate_csv_headers_parse():
    """Headers row is valid CSV and matches expected list."""
    content = generate_csv([])
    lines = content.strip().split("\n")
    assert len(lines) == 1
    first_row = next(csv.reader([lines[0]]))
    assert first_row == EXPECTED_CSV_HEADERS


def test_generate_csv_data_rows_contain_expected_fields(sample_job_response):
    """Data rows contain expected job fields."""
    jobs = [sample_job_response]
    content = generate_csv(jobs)
    lines = content.strip().split("\n")
    assert len(lines) == 2  # header + one data row
    rows = list(csv.reader(lines))
    assert len(rows[1]) == len(EXPECTED_CSV_HEADERS)
    assert rows[1][1] == sample_job_response.title
    assert rows[1][2] == sample_job_response.company
    assert rows[1][4] == sample_job_response.date_applied
    assert rows[1][5] == sample_job_response.status
    assert rows[1][6] == sample_job_response.work_model
    assert rows[1][7] == sample_job_response.salary_range
    assert rows[1][8] == sample_job_response.salary_frequency
    assert rows[1][10] == sample_job_response.notes


def test_generate_csv_special_character_escaping_quotes_and_commas():
    """Notes with quotes and commas produce valid CSV (QUOTE_ALL)."""
    from datetime import datetime

    now = datetime(2025, 2, 20, 12, 0, 0)
    job = JobResponse(
        id=1,
        title="Test",
        company="Co",
        url=None,
        date_applied="2025-02-15",
        status="Saved",
        work_model=None,
        salary_range=None,
        salary_frequency="Yearly",
        tech_stack=[],
        notes='He said, "Hello, world!"',
        screenshot_url=None,
        resume_url=None,
        cover_letter_url=None,
        attachments=[],
        created_at=now,
        updated_at=now,
    )
    content = generate_csv([job])
    # Should be parseable and the notes field should round-trip
    rows = list(csv.reader(content.splitlines()))
    assert len(rows) >= 2
    parsed_notes = rows[1][10]
    assert parsed_notes == 'He said, "Hello, world!"'
    # Ensure no broken CSV (e.g. unescaped newline)
    assert content.count("\n") >= 1


def test_generate_csv_null_handling_empty_strings():
    """work_model, salary_range, salary_frequency None -> empty string in CSV."""
    from datetime import datetime

    now = datetime(2025, 2, 20, 12, 0, 0)
    job = JobResponse(
        id=1,
        title="Test",
        company="Co",
        url=None,
        date_applied="2025-02-15",
        status="Saved",
        work_model=None,
        salary_range=None,
        salary_frequency="Yearly",
        tech_stack=[],
        notes=None,
        screenshot_url=None,
        resume_url=None,
        cover_letter_url=None,
        attachments=[],
        created_at=now,
        updated_at=now,
    )
    content = generate_csv([job])
    rows = list(csv.reader(content.splitlines()))
    assert len(rows) == 2
    data_row = rows[1]
    # work_model -> index 6, salary_range -> 7, salary_frequency -> 8
    assert data_row[6] == ""
    assert data_row[7] == ""
    assert data_row[8] == "Yearly"  # default, not None
    # Optional notes empty
    assert data_row[10] == ""


# --- 4.3 generate_json ---


def test_generate_json_preserves_tech_stack_and_attachments_as_arrays(
    sample_job_response_with_nested,
):
    """Nested tech_stack and attachments preserved as arrays; round-trips as JSON."""
    jobs = [sample_job_response_with_nested]
    content = generate_json(jobs)
    data = json.loads(content)
    assert isinstance(data, list)
    assert len(data) == 1
    obj = data[0]
    assert obj["tech_stack"] == ["React", "TypeScript"]
    assert obj["attachments"] == [
        {"name": "resume.pdf", "url": "/uploads/resume.pdf"}
    ]
    # Round-trip: re-serialize and parse again
    content2 = json.dumps(data, indent=2)
    data2 = json.loads(content2)
    assert data2[0]["tech_stack"] == ["React", "TypeScript"]
    assert data2[0]["attachments"] == [
        {"name": "resume.pdf", "url": "/uploads/resume.pdf"}
    ]
