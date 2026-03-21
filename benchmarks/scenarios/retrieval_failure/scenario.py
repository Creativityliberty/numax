from __future__ import annotations


def get_scenario() -> dict:
    return {
        "scenario_id": "retrieval_failure",
        "flow": "retrieval_answer",
        "prompt": "Search unknown missing source about NUMAX continuity.",
        "requires_artifact": False,
        "inject_failure": True,
        "requires_resume": False,
        "mutation_scenario": False,
    }
