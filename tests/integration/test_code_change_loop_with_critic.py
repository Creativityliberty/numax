from numax.core.state import NumaxState
from numax.flows.code_change_loop import build_code_change_loop_flow


def test_code_change_loop_with_critic(tmp_path):
    (tmp_path / "main.py").write_text("print('hello')\n", encoding="utf-8")

    state = NumaxState(
        observation={
            "workspace_path": str(tmp_path),
            "search_query": "hello",
            "patch_old_text": "print('hello')",
            "patch_new_text": "print('world')",
            "preview_patch": True,
            "test_command": ["echo", "tests-ok"],
        }
    )

    graph = build_code_change_loop_flow()
    final_state = graph.run(start="workspace_open", state=state)

    review = final_state.world_state.get("code_review", {})
    assert review.get("decision") in {"accept", "revise", "revert"}
    assert final_state.patch_risk is not None
