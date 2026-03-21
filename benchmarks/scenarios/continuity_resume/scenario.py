from __future__ import annotations


def get_scenario() -> dict:
    return {
        "scenario_id": "continuity_resume",
        "flow": "planning_execution",
        "prompt": "Continue the previous reasoning on NUMAX memory continuity.",
        "requires_artifact": False,
        "inject_failure": False,
        "requires_resume": True,
        "mutation_scenario": False,
        "inject_retrieved_context": [
            {
                "source_id": "memory_resume_seed",
                "text": "Previous session discussed working, episodic and semantic memory for NUMAX.",
                "score": 2.0,
            }
        ],
        "inject_tool_history": [
            {"tool": "retrieve.search", "ok": True},
            {"tool": "critic.validate", "ok": True},
        ],
    }
