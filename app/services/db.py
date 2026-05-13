from typing import Optional

import asyncpg

from app.config import settings
from app.logger import get_logger

logger = get_logger(__name__)

_pool: Optional[asyncpg.Pool] = None


async def create_db_pool() -> None:
    global _pool
    _pool = await asyncpg.create_pool(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        min_size=2,
        max_size=10,
    )
    logger.info("Database pool created")


async def close_db_pool() -> None:
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
        logger.info("Database pool closed")


def get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("Database pool is not initialized")
    return _pool


async def execute_query(query: str, *args):
    async with get_pool().acquire() as conn:
        return await conn.fetch(query, *args)


async def execute_query_one(query: str, *args):
    async with get_pool().acquire() as conn:
        return await conn.fetchrow(query, *args)


async def execute_command(query: str, *args) -> None:
    async with get_pool().acquire() as conn:
        await conn.execute(query, *args)


async def execute_command_with_return(query: str, *args):
    async with get_pool().acquire() as conn:
        return await conn.fetchrow(query, *args)


async def execute_many(query: str, args_list: list) -> None:
    async with get_pool().acquire() as conn:
        await conn.executemany(query, args_list)
