"""Integration tests for GET /api/jobs/export (Tasks 4.4, 4.5)."""
from datetime import date
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


async def _mock_get_db():
    """Yield a mock AsyncSession so tests don't need a real DB."""
    yield MagicMock()


@pytest.fixture
def client():
    """TestClient for the FastAPI app with get_db overridden to avoid real DB."""
    from app.database import get_db
    app.dependency_overrides[get_db] = _mock_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def sample_job_response():
    """JobResponse for integration tests (reuse schema)."""
    from datetime import datetime

    from app.schemas.job import JobResponse

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
        tech_stack=["Python"],
        notes="Great role",
        screenshot_url=None,
        resume_url=None,
        cover_letter_url=None,
        attachments=[],
        created_at=now,
        updated_at=now,
    )


# --- 4.4 Integration tests for GET /export ---


def test_export_format_csv_200_content_type_and_disposition(
    client, sample_job_response
):
    """format=csv -> 200, Content-Type contains text/csv, Content-Disposition attachment filename=saved-jobs-YYYY-MM-DD.csv."""
    with patch(
        "app.api.jobs.get_saved_jobs",
        new_callable=AsyncMock,
        return_value=[sample_job_response],
    ):
        response = client.get("/api/jobs/export?format=csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers.get("content-type", "")
    content_disp = response.headers.get("content-disposition", "")
    assert "attachment" in content_disp
    today = date.today().isoformat()
    assert f"filename=saved-jobs-{today}.csv" in content_disp


def test_export_format_json_200_content_type_and_disposition(
    client, sample_job_response
):
    """format=json -> 200, Content-Type application/json, Content-Disposition filename=saved-jobs-YYYY-MM-DD.json."""
    with patch(
        "app.api.jobs.get_saved_jobs",
        new_callable=AsyncMock,
        return_value=[sample_job_response],
    ):
        response = client.get("/api/jobs/export?format=json")
    assert response.status_code == 200
    assert "application/json" in response.headers.get("content-type", "")
    content_disp = response.headers.get("content-disposition", "")
    assert "attachment" in content_disp
    today = date.today().isoformat()
    assert f"filename=saved-jobs-{today}.json" in content_disp


def test_export_empty_saved_jobs_csv_200_header_only(client):
    """Empty saved jobs: format=csv -> 200, body has header row only."""
    with patch(
        "app.api.jobs.get_saved_jobs",
        new_callable=AsyncMock,
        return_value=[],
    ):
        response = client.get("/api/jobs/export?format=csv")
    assert response.status_code == 200
    lines = response.text.strip().split("\n")
    assert len(lines) == 1
    assert "id" in lines[0] and "title" in lines[0]


def test_export_empty_saved_jobs_json_200_empty_array(client):
    """Empty saved jobs: format=json -> 200, body is '[]'."""
    with patch(
        "app.api.jobs.get_saved_jobs",
        new_callable=AsyncMock,
        return_value=[],
    ):
        response = client.get("/api/jobs/export?format=json")
    assert response.status_code == 200
    assert response.text.strip() == "[]"


# --- 4.5 Integration test for 400 ---


def test_export_missing_format_400(client):
    """Request without format query param -> 400. Response body contains error message about format."""
    response = client.get("/api/jobs/export")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "format" in data["detail"].lower()


@pytest.mark.parametrize("invalid_format", ["xml", "pdf", "txt", ""])
def test_export_invalid_format_400(client, invalid_format):
    """Request with format=xml (or other invalid) -> 400. Response body contains error message about format."""
    response = client.get(f"/api/jobs/export?format={invalid_format}")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "format" in data["detail"].lower()
