# Job Tracking API - FastAPI Backend

A FastAPI-based REST API for the job application tracking system.

![feat](https://github.com/user-attachments/assets/e37fcf61-54d2-4010-b61c-9d97ceafcca8)

[![Build](https://github.com/JuanSebastianGB/job-tracking-backend/actions/workflows/main.yml/badge.svg)](https://github.com/JuanSebastianGB/job-tracking-backend)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org)

## Prerequisites

- Python 3.10 or higher
- pnpm (for frontend)

## Setup

1. Navigate to the backend directory:
   ```bash
   cd job-tracking-backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   # On macOS/Linux
   source venv/bin/activate

   # On Windows
   venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. (Optional) Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

## Running the Server

Start the development server with auto-reload:

```bash
uvicorn app.main:app --reload --port 3000
```

The server will start at `http://localhost:3000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/jobs` | Get all jobs |
| POST | `/api/jobs` | Create a new job |
| GET | `/api/jobs/{id}` | Get a specific job |
| PUT | `/api/jobs/{id}` | Update a job |
| DELETE | `/api/jobs/{id}` | Delete a job |
| POST | `/api/upload` | Upload a file |

### Request/Response Examples

**GET /api/jobs**
```json
[
  {
    "id": 1,
    "title": "Software Engineer",
    "company": "Acme Corp",
    "url": "https://acme.com/jobs/1",
    "date_applied": "2024-01-15",
    "status": "Applied",
    "work_model": "Remote",
    "salary_range": "120k-150k",
    "salary_frequency": "Yearly",
    "tech_stack": ["React", "TypeScript", "Node.js"],
    "notes": "Great opportunity",
    "screenshot_url": "/uploads/screenshot.png",
    "resume_url": "/uploads/resume.pdf",
    "cover_letter_url": null,
    "attachments": [],
    "created_at": "2024-01-15T10:00:00",
    "updated_at": "2024-01-15T10:00:00"
  }
]
```

**POST /api/jobs**
```json
{
  "title": "Software Engineer",
  "company": "Acme Corp",
  "url": "https://acme.com/jobs/1",
  "date_applied": "2024-01-15",
  "status": "Applied",
  "work_model": "Remote",
  "salary_range": "120k-150k",
  "salary_frequency": "Yearly",
  "tech_stack": ["React", "TypeScript"],
  "notes": "Great opportunity"
}
```

Response: `{"id": 1}`

**PUT /api/jobs/{id}**
```json
{
  "status": "Interviewing"
}
```

Response: `{"success": true}`

**DELETE /api/jobs/{id}**
Response: `{"success": true}`

**POST /api/upload**
Content-Type: `multipart/form-data`
Field: `file` (file upload)

Response: `{"url": "/uploads/filename.png"}`

## File Uploads

Uploaded files are stored in `job-tracking-backend/uploads/` and served at `/uploads/{filename}`.

## Development

The backend uses PostgreSQL (Neon Serverless) by default. Configure the connection via environment variables in `.env`.

## Troubleshooting

### Port already in use
If port 3000 is in use, specify a different port:
```bash
uvicorn app.main:app --reload --port 3001
```

Then update the frontend proxy in `job-tracking-frontend/vite.config.ts` to point to the new port.

### Database not found
Ensure the database URL in `.env` is correctly configured:
```
DATABASE_URL=postgresql+asyncpg://user:password@host.pooler.us-east-1.aws.neon.tech/dbname?sslmode=require
```

## Tech Stack

| Category | Technology |
|----------|------------|
| Framework | FastAPI |
| Language | Python 3.11+ |
| Database | PostgreSQL (Neon Serverless) |
| ORM | SQLAlchemy 2.0+ |
| File Upload | FastAPI |
