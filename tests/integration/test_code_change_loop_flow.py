from numax.core.state import NumaxState
from numax.flows.code_change_loop import build_code_change_loop_flow


def test_code_change_loop_flow(tmp_path):
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

    assert final_state.last_patch
    assert final_state.last_test_run
    assert final_state.last_patch.get("apply_result", {}).get("ok") is True
