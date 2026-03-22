from __future__ import annotations

from typing import Any, Dict


def adapt_skill_to_catalog_item(
    skill_id: str,
    title: str,
    description: str,
    raw_content: str = "",
) -> Dict[str, Any]:
    return {
        "skill_id": skill_id,
        "title": title,
        "description": description,
        "raw_content": raw_content,
        "tags": [],
    }
