from __future__ import annotations


def get_scenario() -> dict:
    return {
        "scenario_id": "provider_failure",
        "flow": "basic_chat",
        "prompt": "Explain NUMAX under provider failure conditions.",
        "requires_artifact": False,
        "inject_failure": True,
        "provider_failure": True,
        "requires_resume": False,
        "mutation_scenario": False,
        "inject_tool_history": [
            {"tool": "provider.openai", "ok": False},
            {"tool": "provider.mock", "ok": True},
        ],
    }
