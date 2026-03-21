from numax.core.state import NumaxState
from numax.subagents.coder import CoderSubagent


def test_coder_subagent_with_active_files():
    state = NumaxState(active_files=["main.py"])
    result = CoderSubagent().act(state)

    assert result["suggested_action"] in {"read_target_files", "inspect_files", "refine_patch", "apply_patch_real", "repair_after_failure"}
