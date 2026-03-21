from numax.core.state import NumaxState
from numax.flows.workspace_analysis import build_workspace_analysis_flow


def test_workspace_analysis_flow(tmp_path):
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")

    state = NumaxState(
        observation={"workspace_path": str(tmp_path)}
    )

    graph = build_workspace_analysis_flow()
    final_state = graph.run(start="workspace_open", state=state)

    assert final_state.active_workspace
    assert final_state.final_output is not None
