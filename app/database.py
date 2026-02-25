import json
from typing import Any, Dict, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings


def _get_create_engine_kwargs(url: str) -> Dict[str, Any]:
    kwargs: Dict[str, Any] = {
        "echo": False,
        "pool_pre_ping": True,
        "pool_size": 5,
        "max_overflow": 10,
        "json_deserializer": json.loads,  # For PostgreSQL JSONB
    }
    if url.startswith("postgresql+asyncpg"):
        kwargs["connect_args"] = {"ssl": "require"}
    return kwargs


async_engine: AsyncEngine = create_async_engine(
    settings.database_url,
    **_get_create_engine_kwargs(settings.database_url),
)

async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    from app.models import job  # noqa: F401

    async with async_engine.begin() as conn:
        await conn.run_sync(job.Base.metadata.create_all)
