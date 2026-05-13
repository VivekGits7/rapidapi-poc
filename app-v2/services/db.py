"""asyncpg connection pool + ergonomic query helpers.

All dumper and router code goes through these helpers — never spin up a
direct asyncpg connection elsewhere.
"""

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Optional

import asyncpg

from config import settings
from logger import get_logger

logger = get_logger(__name__)

_pool: Optional[asyncpg.Pool] = None


async def create_db_pool() -> None:
    global _pool
    if _pool is not None:
        return
    _pool = await asyncpg.create_pool(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        database=settings.POSTGRES_DB,
        min_size=2,
        max_size=20,
        command_timeout=60,
    )
    logger.info(
        f"Postgres pool created: {settings.POSTGRES_USER}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    )


async def close_db_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
        logger.info("Postgres pool closed")


def _get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("Postgres pool is not initialized — call create_db_pool() first")
    return _pool


# ==================== READ HELPERS ====================

async def execute_query(query: str, *args: Any) -> list[asyncpg.Record]:
    async with _get_pool().acquire() as conn:
        return await conn.fetch(query, *args)


async def execute_query_one(query: str, *args: Any) -> Optional[asyncpg.Record]:
    async with _get_pool().acquire() as conn:
        return await conn.fetchrow(query, *args)


async def execute_scalar(query: str, *args: Any) -> Any:
    """Run a query and return a single scalar (e.g. `nextval`, `count(*)`)."""
    async with _get_pool().acquire() as conn:
        return await conn.fetchval(query, *args)


# ==================== WRITE HELPERS ====================

async def execute_command(query: str, *args: Any) -> str:
    """Run an INSERT/UPDATE/DELETE without returning a row. Returns the status string."""
    async with _get_pool().acquire() as conn:
        return await conn.execute(query, *args)


async def execute_command_with_return(query: str, *args: Any) -> Optional[asyncpg.Record]:
    """Run a write that uses RETURNING. Returns the first returned row (or None)."""
    async with _get_pool().acquire() as conn:
        return await conn.fetchrow(query, *args)


async def execute_many(query: str, rows: list[tuple]) -> None:
    """Batch insert/update. Significantly faster than looping execute_command."""
    if not rows:
        return
    async with _get_pool().acquire() as conn:
        await conn.executemany(query, rows)


# ==================== TRANSACTIONS ====================

@asynccontextmanager
async def transaction() -> AsyncIterator[Any]:
    """Async context manager wrapping a single asyncpg transaction.

    Usage:
        async with transaction() as conn:
            await conn.execute(...)
            await conn.execute(...)
    """
    pool = _get_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            yield conn
