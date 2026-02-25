from datetime import datetime
from typing import Optional, List, Any

from pydantic import BaseModel, ConfigDict


class Attachment(BaseModel):
    name: str
    url: str


class JobBase(BaseModel):
    title: str
    company: str
    url: Optional[str] = None
    date_applied: str
    status: str
    work_model: Optional[str] = None
    salary_range: Optional[str] = None
    salary_frequency: str = "Yearly"
    tech_stack: List[str] = []
    notes: Optional[str] = None
    screenshot_url: Optional[str] = None
    resume_url: Optional[str] = None
    cover_letter_url: Optional[str] = None
    attachments: List[
        Any
    ] = []  # Can be either List[str] or List[dict] for backward compatibility


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    url: Optional[str] = None
    date_applied: Optional[str] = None
    status: Optional[str] = None
    work_model: Optional[str] = None
    salary_range: Optional[str] = None
    salary_frequency: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    notes: Optional[str] = None
    screenshot_url: Optional[str] = None
    resume_url: Optional[str] = None
    cover_letter_url: Optional[str] = None
    attachments: Optional[List[Any]] = None  # Can be either List[str] or List[dict]


class JobResponse(JobBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
