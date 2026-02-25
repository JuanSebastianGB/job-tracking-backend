# Backend (FastAPI) - AI Agent Ruleset

> **Skills Reference**: For detailed patterns, use these skills:
> - [`fastapi-templates`](../.agents/skills/fastapi-templates/SKILL.md) - Production-ready FastAPI projects
> - [`backend-patterns`](../.agents/skills/backend-patterns/SKILL.md) - Node.js/Express/FastAPI patterns
> - [`docker-expert`](../.agents/skills/docker-expert/SKILL.md) - Containerization patterns
> - [`neon-postgres`](../.agents/skills/neon-postgres/SKILL.md) - Neon Serverless Postgres patterns

### Auto-invoke Skills

When performing these actions, ALWAYS invoke the corresponding skill FIRST:

| Action | Skill |
| ------ | ----- |
| Create new FastAPI project | `fastapi-templates` |
| Design REST API endpoints | `backend-patterns` |
| Implement database models | `backend-patterns` |
| Add Docker configuration | `docker-expert` |
| Use postgres database | `neon-postgres` |
| Create git commit | `git-commit` |

---

## CRITICAL RULES - NON-NEGOTIABLE

### FastAPI

- **ALWAYS**: Use Pydantic models for request/response validation
- **ALWAYS**: Use SQLAlchemy ORM for database operations
- **ALWAYS**: Implement proper error handling with HTTPException
- **NEVER**: Expose raw database errors to clients
- **ALWAYS**: Use async/await for I/O operations

### Python

- **ALWAYS**: Use type hints for function arguments and return values
- **ALWAYS**: Use `pydantic` for data validation
- **ALWAYS**: Use proper HTTP status codes (200, 201, 400, 404, 500)
- **NEVER**: Use `print()` for debugging - use `logging`

### Database

- **ALWAYS**: Use migrations (Alembic) for schema changes
- **ALWAYS**: Use dependency injection for database sessions
- **ALWAYS**: Handle connection errors gracefully

---

## DECISION TREES

### New Endpoint

```
CRUD operation? → Use ViewSet pattern from backend-patterns
                → Create router in app/api/
                → Add model in app/models/
                → Add schema in app/schemas/

Simple endpoint? → Add to existing router
```

### Code Location

```
Routes → app/api/
Models → app/models/
Schemas → app/schemas/
Business logic → app/services/
Utilities → app/utils/
```

---

## PATTERNS

### Pydantic Schema

```python
from pydantic import BaseModel, Field
from datetime import datetime

class JobBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=200)
    status: str = Field(default="applied")

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: int
    created_at: datetime
    
    model_config = {"from_attributes": True}
```

### API Endpoint

```python
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import JobCreate, JobResponse
from app.models import Job

router = APIRouter()

@router.post("/jobs", response_model=JobResponse, status_code=201)
async def create_job(job: JobCreate, db: Session = Depends(get_db)):
    db_job = Job(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
```

### Error Handling

```python
from fastapi import HTTPException

@router.delete("/jobs/{job_id}")
async def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.delete(job)
    db.commit()
    return {"message": "Job deleted"}
```

---

## TECH STACK

FastAPI 0.109+ | SQLAlchemy 2.0+ | Pydantic 2.0+ | Python 3.11+

---

## PROJECT STRUCTURE

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app entry point
│   ├── config.py         # Configuration settings
│   ├── database.py       # Database connection
│   ├── api/              # API routes
│   │   └── v1/
│   │       └── jobs.py   # Job endpoints
│   ├── models/           # SQLAlchemy models
│   │   └── job.py
│   ├── schemas/          # Pydantic schemas
│   │   └── job.py
│   ├── services/        # Business logic
│   │   └── job_service.py
│   └── utils/           # Utilities
├── requirements.txt
└── .env
```

---

## COMMANDS

```bash
# Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --port 8000

# Run with Docker
docker build -t job-tracker-backend .
docker run -p 8000:8000 job-tracker-backend
```

---

## QA CHECKLIST BEFORE COMMIT

- [ ] All endpoints have proper Pydantic validation
- [ ] HTTPException used for error handling
- [ ] No raw database errors exposed to clients
- [ ] Database sessions properly managed (dependency injection)
- [ ] Type hints on all functions
- [ ] No hardcoded secrets (use environment variables)
- [ ] API follows REST conventions
- [ ] Models have proper relationships defined
