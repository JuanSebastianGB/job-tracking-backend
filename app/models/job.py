from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    url = Column(String, nullable=True)
    date_applied = Column(String, nullable=False)
    status = Column(String, nullable=False)
    work_model = Column(String, nullable=True)
    salary_range = Column(String, nullable=True)
    salary_frequency = Column(String, default="Yearly")
    tech_stack = Column(JSONB, nullable=True)
    notes = Column(Text, nullable=True)
    screenshot_url = Column(String, nullable=True)
    resume_url = Column(String, nullable=True)
    cover_letter_url = Column(String, nullable=True)
    attachments = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
