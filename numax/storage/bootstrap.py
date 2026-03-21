from __future__ import annotations

import os

from numax.storage.base import KeyValueStore
from numax.storage.local_json import LocalJsonStore
from numax.storage.sqlite import SQLiteStore


def build_default_store() -> KeyValueStore:
    backend = os.getenv("NUMAX_STORE_BACKEND", "json").lower()

    if backend == "sqlite":
        return SQLiteStore(db_path=os.getenv("NUMAX_SQLITE_PATH", "data/store/numax.db"))

    if backend == "redis":
        import redis  # type: ignore

        from numax.storage.redis_store import RedisStore

        client = redis.Redis.from_url(os.getenv("NUMAX_REDIS_URL", "redis://localhost:6379/0"))
        return RedisStore(client=client)

    if backend == "postgres":
        import psycopg  # type: ignore

        from numax.storage.postgres_store import PostgresStore

        conn = psycopg.connect(os.getenv("NUMAX_POSTGRES_DSN", "postgresql://localhost/numax"))
        return PostgresStore(conn=conn)

    return LocalJsonStore(root_dir="data/store")
