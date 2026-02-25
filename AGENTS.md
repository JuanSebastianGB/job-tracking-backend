# AGENTS.md

## The Role

This file describes rules, patterns, and conventions for AI agents working on the job-tracking backend (FastAPI). It also maps actions to specialized skills that should be invoked for specific tasks.

> **IMPORTANT**: If you encounter something surprising or non-obvious in this codebase, alert the developer and document it in this file to help future agents.

---

## Skills Mapping

### Available Skills

| Skill | Description | Location |
| ----- | ----------- | -------- |
| `fastapi-templates` | Production-ready FastAPI projects | `.agents/skills/fastapi-templates/SKILL.md` |
| `backend-patterns` | Node.js/Express/FastAPI patterns | `.agents/skills/backend-patterns/SKILL.md` |
| `docker-expert` | Containerization patterns | `.agents/skills/docker-expert/SKILL.md` |
| `neon-postgres` | Neon Serverless Postgres patterns | `.agents/skills/neon-postgres/SKILL.md` |
| `git-commit` | Professional commit conventions | `~/.opencode/skills/git-commit/SKILL.md` |
| `crafting-effective-readmes` | README templates | `.agents/skills/crafting-effective-readmes/SKILL.md` |

### Action-to-Skill Mappings

| Action | Skill |
| ------ | ----- |
| Create new FastAPI project | `fastapi-templates` |
| Design REST API endpoints | `backend-patterns` |
| Implement database models | `backend-patterns` |
| Add Docker configuration | `docker-expert` |
| Use postgres database | `neon-postgres` |
| Create git commit | `git-commit` |
| Write or update README | `crafting-effective-readmes` |
