from __future__ import annotations

import json
from typing import Any

from numax.storage.base import KeyValueStore


class RedisStore(KeyValueStore):
    def __init__(self, client: Any) -> None:
        self.client = client

    def get(self, key: str, default: Any = None) -> Any:
        value = self.client.get(key)
        if value is None:
            return default
        try:
            if isinstance(value, bytes):
                value = value.decode("utf-8")
            return json.loads(value)
        except Exception:
            return default

    def set(self, key: str, value: Any) -> None:
        self.client.set(key, json.dumps(value))

    def delete(self, key: str) -> None:
        self.client.delete(key)

    def list_keys(self) -> list[str]:
        keys = self.client.keys("*")
        out = []
        for key in keys:
            if isinstance(key, bytes):
                out.append(key.decode("utf-8"))
            else:
                out.append(str(key))
        return sorted(out)
