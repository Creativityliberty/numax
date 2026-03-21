from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from numax.storage.base import KeyValueStore


class SQLiteStore(KeyValueStore):
    def __init__(self, db_path: str = "data/store/numax.db") -> None:
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS kv_store (k TEXT PRIMARY KEY, v TEXT NOT NULL)"
        )
        self.conn.commit()

    def get(self, key: str, default: Any = None) -> Any:
        cur = self.conn.execute("SELECT v FROM kv_store WHERE k = ?", (key,))
        row = cur.fetchone()
        if not row:
            return default
        try:
            return json.loads(row[0])
        except Exception:
            return default

    def set(self, key: str, value: Any) -> None:
        payload = json.dumps(value)
        self.conn.execute(
            "INSERT INTO kv_store(k, v) VALUES(?, ?) ON CONFLICT(k) DO UPDATE SET v=excluded.v",
            (key, payload),
        )
        self.conn.commit()

    def delete(self, key: str) -> None:
        self.conn.execute("DELETE FROM kv_store WHERE k = ?", (key,))
        self.conn.commit()

    def list_keys(self) -> list[str]:
        cur = self.conn.execute("SELECT k FROM kv_store ORDER BY k ASC")
        return [row[0] for row in cur.fetchall()]
