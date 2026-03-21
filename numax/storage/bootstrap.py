from __future__ import annotations

from numax.storage.local_json import LocalJsonStore


def build_default_store() -> LocalJsonStore:
    return LocalJsonStore(root_dir="data/store")
