import csv
import io
import json
from typing import List

from app.schemas.job import JobResponse


def generate_csv(jobs: List[JobResponse]) -> str:
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)

    writer.writerow(
        [
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
    )

    def _cell(value):
        if value is None:
            return ""
        if isinstance(value, (list, dict)):
            return json.dumps(value)
        if hasattr(value, "isoformat"):
            return value.isoformat()
        return value

    for job in jobs:
        writer.writerow(
            [
                job.id,
                job.title,
                job.company,
                job.url or "",
                job.date_applied,
                job.status,
                job.work_model or "",
                job.salary_range or "",
                job.salary_frequency or "",
                _cell(job.tech_stack),
                job.notes or "",
                job.screenshot_url or "",
                job.resume_url or "",
                job.cover_letter_url or "",
                _cell(job.attachments),
                _cell(job.created_at),
                _cell(job.updated_at),
            ]
        )

    return output.getvalue()


def generate_json(jobs: List[JobResponse]) -> str:
    return json.dumps(
        [job.model_dump(mode="json") for job in jobs],
        indent=2,
        default=str,
    )
