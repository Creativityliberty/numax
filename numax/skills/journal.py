from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SKILL_JOURNAL_PATH = Path("data/state/skills_journal.json")
SKILL_JOURNAL_PATH.parent.mkdir(parents=True, exist_ok=True)


DEFAULT_JOURNAL: dict[str, Any] = {
    "entries": [],
    "last_known_good": [],
}


def load_skill_journal() -> dict[str, Any]:
    if not SKILL_JOURNAL_PATH.exists():
        return dict(DEFAULT_JOURNAL)
    try:
        data = json.loads(SKILL_JOURNAL_PATH.read_text(encoding="utf-8"))
        return {**DEFAULT_JOURNAL, **(data or {})}
    except Exception:
        return dict(DEFAULT_JOURNAL)


def save_skill_journal(journal: dict[str, Any]) -> None:
    SKILL_JOURNAL_PATH.write_text(json.dumps(journal, indent=2), encoding="utf-8")


def current_installed_skills() -> list[str]:
    journal = load_skill_journal()
    installed: list[str] = []
    for entry in journal.get("entries", []):
        action = entry.get("action")
        skill_id = entry.get("skill_id")
        if action == "apply" and skill_id not in installed:
            installed.append(skill_id)
        if action == "uninstall" and skill_id in installed:
            installed.remove(skill_id)
    return installed


def mark_last_known_good(skills: list[str]) -> dict[str, Any]:
    journal = load_skill_journal()
    journal["last_known_good"] = list(skills)
    save_skill_journal(journal)
    return journal


def append_entry(entry: dict[str, Any]) -> dict[str, Any]:
    journal = load_skill_journal()
    journal.setdefault("entries", []).append(entry)
    save_skill_journal(journal)
    return journal
