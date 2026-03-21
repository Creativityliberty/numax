from __future__ import annotations

from numax.storage.base import KeyValueStore


class SessionRepository:
    def __init__(self, store: KeyValueStore) -> None:
        self.store = store

    def get(self, session_id: str) -> dict | None:
        res = self.store.get(f"sessions/{session_id}")
        return res if isinstance(res, dict) else None

    def save(self, session_id: str, payload: dict) -> None:
        self.store.set(f"sessions/{session_id}", payload)


class PolicyRepository:
    def __init__(self, store: KeyValueStore) -> None:
        self.store = store

    def get(self, name: str, default: dict | None = None) -> dict:
        res = self.store.get(f"policies/{name}", default or {})
        return res if isinstance(res, dict) else {}

    def save(self, name: str, payload: dict) -> None:
        self.store.set(f"policies/{name}", payload)
