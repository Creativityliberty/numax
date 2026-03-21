from __future__ import annotations


def get_scenario() -> dict:
    return {
        "scenario_id": "provider_failure",
        "flow": "basic_chat",
        "prompt": "Explain NUMAX under provider pressure.",
        "requires_artifact": False,
        "inject_failure": True,
        "requires_resume": False,
        "mutation_scenario": False,
    }
