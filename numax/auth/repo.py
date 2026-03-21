from __future__ import annotations

from typing import Any

from numax.auth.models import UserIdentity
from numax.storage.base import KeyValueStore


class UserRepository:
    def __init__(self, store: KeyValueStore) -> None:
        self.store = store

    def save(self, user: UserIdentity) -> None:
        self.store.set(f"users/{user.user_id}", user.model_dump())

    def get(self, user_id: str) -> dict[str, Any] | None:
        res = self.store.get(f"users/{user_id}")
        return res if isinstance(res, dict) else None

    def list_all(self) -> list[dict]:
        rows = []
        for key in self.store.list_keys():
            if key.startswith("users/"):
                item = self.store.get(key)
                if item:
                    rows.append(item)
        return rows
