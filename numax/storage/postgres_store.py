from __future__ import annotations

import json
from typing import Any

from numax.storage.base import KeyValueStore


class PostgresStore(KeyValueStore):
    def __init__(self, conn: Any) -> None:
        self.conn = conn
        self._init_schema()

    def _init_schema(self) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS kv_store (
                    k TEXT PRIMARY KEY,
                    v JSONB NOT NULL
                )
                """
            )
        self.conn.commit()

    def get(self, key: str, default: Any = None) -> Any:
        with self.conn.cursor() as cur:
            cur.execute("SELECT v FROM kv_store WHERE k = %s", (key,))
            row = cur.fetchone()
        if not row:
            return default
        return row[0]

    def set(self, key: str, value: Any) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO kv_store(k, v)
                VALUES (%s, %s)
                ON CONFLICT (k) DO UPDATE SET v = EXCLUDED.v
                """,
                (key, json.dumps(value)),
            )
        self.conn.commit()

    def delete(self, key: str) -> None:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM kv_store WHERE k = %s", (key,))
        self.conn.commit()

    def list_keys(self) -> list[str]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT k FROM kv_store ORDER BY k ASC")
            rows = cur.fetchall()
        return [row[0] for row in rows]
