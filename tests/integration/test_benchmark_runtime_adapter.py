from benchmarks.runtime_adapter import run_numax_scenario


def test_run_numax_scenario_memory_resume():
    scenario = {
        "scenario_id": "continuity_resume",
        "flow": "planning_execution",
        "prompt": "Continue NUMAX memory reasoning",
        "inject_retrieved_context": [
            {"source_id": "seed", "text": "NUMAX has episodic and semantic memory.", "score": 2.0}
        ],
        "inject_tool_history": [
            {"tool": "retrieve.search", "ok": True},
            {"tool": "critic.validate", "ok": True},
        ],
    }

    result = run_numax_scenario(scenario)

    assert result["system"] == "numax"
    assert result["continuity_score"] >= 0.5
    assert "memory_policy" in result


def test_run_numax_scenario_mutation_pipeline():
    scenario = {
        "scenario_id": "mutation_rollback",
        "flow": "basic_chat",
        "prompt": "Explain NUMAX rollback",
        "mutation_scenario": True,
    }

    result = run_numax_scenario(scenario)

    assert result["replay_ok"] is True
    assert result["rollback_ok"] is True
