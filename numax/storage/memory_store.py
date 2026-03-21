from __future__ import annotations

from typing import Any

from numax.storage.base import KeyValueStore


class InMemoryStore(KeyValueStore):
    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def delete(self, key: str) -> None:
        self._data.pop(key, None)

    def list_keys(self) -> list[str]:
        return sorted(self._data.keys())
