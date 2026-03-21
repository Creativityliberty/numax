from __future__ import annotations


def get_scenario() -> dict:
    return {
        "scenario_id": "long_task",
        "flow": "artifact_output",
        "prompt": "Search and explain the memory mechanisms of NUMAX, then produce a structured summary artifact.",
        "requires_artifact": True,
        "inject_failure": False,
        "requires_resume": False,
        "mutation_scenario": False,
    }
