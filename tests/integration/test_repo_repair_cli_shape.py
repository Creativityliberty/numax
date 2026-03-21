from numax.core.state import NumaxState
from numax.flows.repo_repair import build_repo_repair_flow


def test_repo_repair_flow_runs(tmp_path):
    (tmp_path / "README.md").write_text("broken hello", encoding="utf-8")

    state = NumaxState(
        observation={
            "workspace_path": str(tmp_path),
            "search_query": "hello",
            "patch_old_text": "hello",
            "patch_new_text": "world",
            "preview_patch": True,
            "test_command": ["echo", "ok"],
        }
    )

    graph = build_repo_repair_flow()
    final_state = graph.run(start="workspace_open", state=state)

    assert final_state.next_recommended_action in {"critic_review", "inspect_test_failure"}
