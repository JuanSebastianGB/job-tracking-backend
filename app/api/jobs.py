from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.job import JobCreate, JobUpdate, JobResponse
from app.services.job_service import (
    create_job,
    get_jobs,
    get_job,
    update_job,
    delete_job,
)

jobs_router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@jobs_router.get("/", response_model=List[JobResponse])
async def list_jobs(db: AsyncSession = Depends(get_db)):
    return await get_jobs(db)


@jobs_router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_job_endpoint(job: JobCreate, db: AsyncSession = Depends(get_db)):
    created_job = await create_job(db, job)
    return {"id": created_job.id}


@jobs_router.get("/{job_id}", response_model=JobResponse)
async def get_job_endpoint(job_id: int, db: AsyncSession = Depends(get_db)):
    job = await get_job(db, job_id)
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )
    return job


@jobs_router.put("/{job_id}", response_model=dict)
async def update_job_endpoint(
    job_id: int, job: JobUpdate, db: AsyncSession = Depends(get_db)
):
    updated_job = await update_job(db, job_id, job)
    if updated_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )
    return {"success": True}


@jobs_router.delete("/{job_id}", response_model=dict)
async def delete_job_endpoint(job_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_job(db, job_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )
    return {"success": True}
