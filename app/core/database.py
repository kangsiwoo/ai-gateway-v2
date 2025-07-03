import asyncpg
from typing import Optional, List, Dict
from .config import settings

_db_pool: Optional[asyncpg.pool.Pool] = None

async def connect_db():
    global _db_pool
    if _db_pool is None:
        _db_pool = await asyncpg.create_pool(
            dsn=settings.db_url,
            user=settings.db_username,
            password=settings.db_password,
        )
        await init_db()

async def close_db():
    global _db_pool
    if _db_pool is not None:
        await _db_pool.close()
        _db_pool = None

async def init_db():
    assert _db_pool is not None
    async with _db_pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS servers (
                server_id TEXT PRIMARY KEY,
                url TEXT NOT NULL
            )
            """
        )

async def add_server(server_id: str, url: str):
    assert _db_pool is not None
    async with _db_pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO servers(server_id, url) VALUES($1, $2) ON CONFLICT (server_id) DO NOTHING",
            server_id,
            url,
        )

async def remove_server(server_id: str):
    assert _db_pool is not None
    async with _db_pool.acquire() as conn:
        await conn.execute("DELETE FROM servers WHERE server_id=$1", server_id)

async def fetch_servers() -> List[Dict[str, str]]:
    assert _db_pool is not None
    async with _db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT server_id, url FROM servers")
        return [{"server_id": r["server_id"], "url": r["url"]} for r in rows]
