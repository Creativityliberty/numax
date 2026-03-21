from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from numax.storage.base import KeyValueStore


class LocalJsonStore(KeyValueStore):
    def __init__(self, root_dir: str = "data/store") -> None:
        self.root = Path(root_dir)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        safe = key.replace("/", "__")
        return self.root / f"{safe}.json"

    def get(self, key: str, default: Any = None) -> Any:
        path = self._path(key)
        if not path.exists():
            return default
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return default

    def set(self, key: str, value: Any) -> None:
        self._path(key).write_text(json.dumps(value, indent=2), encoding="utf-8")

    def delete(self, key: str) -> None:
        path = self._path(key)
        if path.exists():
            path.unlink()

    def list_keys(self) -> list[str]:
        keys = []
        for file in self.root.glob("*.json"):
            keys.append(file.stem.replace("__", "/"))
        return sorted(keys)
