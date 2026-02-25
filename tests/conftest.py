"""Shared fixtures for backend tests."""
from datetime import datetime

import pytest

from app.schemas.job import JobResponse


@pytest.fixture
def sample_job_response():
    """JobResponse fixture with fixed dates for reproducible tests."""
    now = datetime(2025, 2, 20, 12, 0, 0)
    return JobResponse(
        id=1,
        title="Backend Engineer",
        company="Acme Corp",
        url="https://example.com/job/1",
        date_applied="2025-02-15",
        status="Saved",
        work_model="Remote",
        salary_range="$100k-$150k",
        salary_frequency="Yearly",
        tech_stack=["Python", "FastAPI"],
        notes="Great role",
        screenshot_url=None,
        resume_url=None,
        cover_letter_url=None,
        attachments=[],
        created_at=now,
        updated_at=now,
    )


@pytest.fixture
def sample_job_response_with_nested():
    """JobResponse with tech_stack and attachments as arrays for JSON round-trip tests."""
    now = datetime(2025, 2, 20, 12, 0, 0)
    return JobResponse(
        id=2,
        title="Frontend Dev",
        company="Beta Inc",
        url="https://example.com/job/2",
        date_applied="2025-02-10",
        status="Saved",
        work_model=None,
        salary_range=None,
        salary_frequency="Yearly",
        tech_stack=["React", "TypeScript"],
        notes=None,
        screenshot_url=None,
        resume_url=None,
        cover_letter_url=None,
        attachments=[{"name": "resume.pdf", "url": "/uploads/resume.pdf"}],
        created_at=now,
        updated_at=now,
    )
