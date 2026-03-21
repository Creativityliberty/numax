from __future__ import annotations

import os

from numax.storage.local_json import LocalJsonStore
from numax.storage.sqlite import SQLiteStore


def build_default_store() -> SQLiteStore | LocalJsonStore:
    backend = os.getenv("NUMAX_STORE_BACKEND", "json").lower()
    if backend == "sqlite":
        return SQLiteStore(db_path=os.getenv("NUMAX_SQLITE_PATH", "data/store/numax.db"))
    return LocalJsonStore(root_dir="data/store")
