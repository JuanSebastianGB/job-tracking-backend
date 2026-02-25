"""Unit tests for job_service.get_saved_jobs (Task 4.1)."""
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from app.models.job import Job
from app.schemas.job import JobResponse
from app.services.job_service import get_saved_jobs


@pytest.mark.asyncio
async def test_get_saved_jobs_filters_by_status_saved_and_orders_by_date_applied_desc():
    """Verify get_saved_jobs uses select with Job.status == 'Saved' and order_by date_applied.desc()."""
    # Arrange: mock Job instances
    now = datetime(2025, 2, 20, 12, 0, 0)
    mock_job = MagicMock(spec=Job)
    mock_job.id = 1
    mock_job.title = "Engineer"
    mock_job.company = "Acme"
    mock_job.url = None
    mock_job.date_applied = "2025-02-15"
    mock_job.status = "Saved"
    mock_job.work_model = None
    mock_job.salary_range = None
    mock_job.salary_frequency = "Yearly"
    mock_job.tech_stack = []
    mock_job.notes = None
    mock_job.screenshot_url = None
    mock_job.resume_url = None
    mock_job.cover_letter_url = None
    mock_job.attachments = []
    mock_job.created_at = now
    mock_job.updated_at = now

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_job]

    mock_db = AsyncMock()
    mock_db.execute = AsyncMock(return_value=mock_result)

    # Act
    result = await get_saved_jobs(mock_db)

    # Assert: execute was called once with a select statement filtering status and ordering
    assert mock_db.execute.await_count == 1
    call_args = mock_db.execute.await_args
    statement = call_args[0][0]
    stmt_str = str(statement).lower()
    assert "status" in stmt_str
    assert "date_applied" in stmt_str
    assert "desc" in stmt_str
    # Bound param value (SQLAlchemy uses :status_1, not literal "saved" in the string)
    compiled = statement.compile()
    assert "Saved" in compiled.params.values()

    # Assert: return value is list of JobResponse-shaped items
    assert len(result) == 1
    assert isinstance(result[0], JobResponse)
    assert result[0].id == 1
    assert result[0].title == "Engineer"
    assert result[0].company == "Acme"
    assert result[0].status == "Saved"
    assert result[0].date_applied == "2025-02-15"


@pytest.mark.asyncio
async def test_get_saved_jobs_returns_empty_list_when_no_saved_jobs():
    """Return value is empty list when no jobs match."""
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []

    mock_db = AsyncMock()
    mock_db.execute = AsyncMock(return_value=mock_result)

    result = await get_saved_jobs(mock_db)

    assert result == []
    assert mock_db.execute.await_count == 1
