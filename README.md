# JobTracker API - Backend

> A FastAPI-powered REST API for the job application tracking system with PostgreSQL persistence.

![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-336791?logo=postgresql)

## What This Does

The JobTracker API provides a RESTful interface for storing, retrieving, and managing job applications. It handles CRUD operations, file uploads, and integrates with Neon Serverless PostgreSQL for persistent storage.

## Quick Start

```bash
# Navigate to the backend
cd job-tracking-backend

# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Start the server
uvicorn app.main:app --reload --port 3000
```

That's it! The API will be running at **http://localhost:3000**

> 📖 API docs available at **http://localhost:3000/docs** (Swagger UI)

## Configuration

Create a `.env` file in `job-tracking-backend/` with your database connection:

```env
# Neon PostgreSQL connection string
DATABASE_URL=postgresql+asyncpg://user:password@host.pooler.us-east-1.aws.neon.tech/dbname?sslmode=require
```

Get your free database from [Neon](https://neon.tech).

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/jobs` | List all job applications |
| `POST` | `/api/jobs` | Create a new job application |
| `GET` | `/api/jobs/{id}` | Get a specific job |
| `PUT` | `/api/jobs/{id}` | Update a job |
| `DELETE` | `/api/jobs/{id}` | Delete a job |
| `POST` | `/api/upload` | Upload a file (resume, screenshot, etc.) |

### Example Requests & Responses

#### GET /api/jobs
```json
[
  {
    "id": 1,
    "title": "Senior Software Engineer",
    "company": "Acme Corp",
    "url": "https://acme.com/jobs/123",
    "date_applied": "2024-01-15",
    "status": "Interviewing",
    "work_model": "Remote",
    "salary_range": "120k-150k",
    "salary_frequency": "Yearly",
    "tech_stack": ["React", "TypeScript", "Node.js"],
    "notes": "Great opportunity!",
    "screenshot_url": "/uploads/screenshot.png",
    "resume_url": "/uploads/resume.pdf",
    "cover_letter_url": null,
    "created_at": "2024-01-15T10:00:00",
    "updated_at": "2024-01-15T10:00:00"
  }
]
```

#### POST /api/jobs
```json
{
  "title": "Senior Software Engineer",
  "company": "Acme Corp",
  "url": "https://acme.com/jobs/123",
  "date_applied": "2024-01-15",
  "status": "Applied",
  "work_model": "Remote",
  "salary_range": "120k-150k",
  "salary_frequency": "Yearly",
  "tech_stack": ["React", "TypeScript"],
  "notes": "Looking forward to hearing back!"
}
```
Response: `{"id": 1, "message": "Job created successfully"}`

#### PUT /api/jobs/{id}
```json
{
  "status": "Interviewing"
}
```
Response: `{"success": true, "message": "Job updated"}`

#### DELETE /api/jobs/{id}
Response: `{"success": true, "message": "Job deleted"}`

#### POST /api/upload
- Content-Type: `multipart/form-data`
- Field: `file`

Response: `{"url": "/uploads/filename.png", "message": "File uploaded"}`

## Project Structure

```
job-tracking-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration & environment variables
│   ├── database.py         # SQLAlchemy database connection
│   ├── api/                 # API route handlers
│   │   └── v1/
│   │       └── jobs.py     # Job CRUD endpoints
│   ├── models/              # SQLAlchemy ORM models
│   │   └── job.py
│   ├── schemas/             # Pydantic request/response models
│   │   └── job.py
│   └── services/           # Business logic
│       └── job_service.py
├── uploads/                 # Uploaded files (resumes, screenshots)
├── requirements.txt
└── .env
```

## Tech Stack

| Category | Technology | Why |
|----------|------------|-----|
| Framework | FastAPI | Modern, fast, async Python web framework |
| Language | Python 3.11+ | Type hints, better performance |
| Database | PostgreSQL (Neon) | Serverless, scales automatically |
| ORM | SQLAlchemy 2.0 | Async support, type-safe queries |
| Validation | Pydantic 2.0 | Data validation & serialization |
| Server | Uvicorn | ASGI server implementation |

## Key Features

- **Async/Await** - Fully async for better performance
- **Type Safety** - Full Pydantic validation on requests/responses
- **RESTful Design** - Standard HTTP methods and status codes
- **File Uploads** - Support for resumes, screenshots, cover letters
- **Auto-generated Docs** - Interactive API documentation at `/docs`

## Interactive API Docs

FastAPI automatically generates interactive documentation:

- **Swagger UI**: http://localhost:3000/docs
- **ReDoc**: http://localhost:3000/redoc

You can test all endpoints directly from the browser!

## Available Scripts

```bash
# Start development server (with auto-reload)
uvicorn app.main:app --reload --port 3000

# Run with custom host/port
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run with Docker
docker build -t job-tracker-backend .
docker run -p 3000:3000 -e DATABASE_URL=... job-tracker-backend
```

## Troubleshooting

### Port already in use
```bash
# Find process using port 3000
lsof -i :3000

# Or run on a different port
uvicorn app.main:app --reload --port 3001
```

> ⚠️ Don't forget to update the frontend proxy in `vite.config.ts` to point to the new port!

### Database connection failed
- Verify your `DATABASE_URL` in `.env` is correct
- Ensure Neon project is active and not paused
- Check SSL requirements: `?sslmode=require`

### Missing dependencies
```bash
# Reinstall all dependencies
pip install -r requirements.txt
```

### Module not found errors
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall in editable mode
pip install -e .
```

## Database Schema

```
jobs table:
├── id (SERIAL PRIMARY KEY)
├── title (VARCHAR)
├── company (VARCHAR)
├── url (VARCHAR, nullable)
├── date_applied (DATE)
├── status (VARCHAR)
├── work_model (VARCHAR, nullable)
├── salary_range (VARCHAR, nullable)
├── salary_frequency (VARCHAR, nullable)
├── tech_stack (JSON array, nullable)
├── notes (TEXT, nullable)
├── screenshot_url (VARCHAR, nullable)
├── resume_url (VARCHAR, nullable)
├── cover_letter_url (VARCHAR, nullable)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
```

## License

Personal project. Built for learning and personal use.

---

<p align="center">
  Built with 💙 using FastAPI & PostgreSQL
</p>
