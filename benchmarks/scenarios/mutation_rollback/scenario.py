from __future__ import annotations


def get_scenario() -> dict:
    return {
        "scenario_id": "mutation_rollback",
        "flow": "basic_chat",
        "prompt": "Explain how NUMAX should rollback a failed mutation.",
        "requires_artifact": False,
        "inject_failure": True,
        "requires_resume": False,
        "mutation_scenario": True,
    }
