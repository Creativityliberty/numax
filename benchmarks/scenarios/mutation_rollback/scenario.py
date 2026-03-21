from __future__ import annotations


def get_scenario() -> dict:
    return {
        "scenario_id": "mutation_rollback",
        "flow": "basic_chat",
        "prompt": "Explain how NUMAX should rollback and replay a failed mutation.",
        "requires_artifact": False,
        "inject_failure": True,
        "requires_resume": False,
        "mutation_scenario": True,
        "inject_tool_history": [
            {"tool": "skills.apply", "ok": False},
            {"tool": "release.rollback", "ok": True},
        ],
    }
