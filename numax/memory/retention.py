from __future__ import annotations

from typing import Any


def retention_policy(memory_store: dict[str, Any]) -> dict[str, Any]:
    return {
        "working_max_items": 25,
        "episodic_max_items": 200,
        "semantic_max_items": 500,
        "archive_old_episodic": True,
    }


def trim_memory(memory_store: dict[str, Any]) -> dict[str, Any]:
    policy = retention_policy(memory_store)

    episodic = memory_store.setdefault("episodic", [])
    semantic = memory_store.setdefault("semantic", [])

    if len(episodic) > policy["episodic_max_items"]:
        memory_store["episodic"] = episodic[-policy["episodic_max_items"] :]

    if len(semantic) > policy["semantic_max_items"]:
        memory_store["semantic"] = semantic[-policy["semantic_max_items"] :]

    return memory_store
