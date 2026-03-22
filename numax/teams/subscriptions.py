from __future__ import annotations

from typing import Dict, List


DEFAULT_SUBSCRIPTIONS = {
    "spec": ["engineering_squad"],
    "patch": ["qa_squad"],
    "review": ["release_squad"],
    "artifact": ["qa_squad"],
}


def get_subscribers(artifact_type: str) -> list[str]:
    return DEFAULT_SUBSCRIPTIONS.get(artifact_type, [])
