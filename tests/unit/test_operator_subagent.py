from numax.core.state import NumaxState
from numax.subagents.operator import OperatorSubagent


def test_operator_subagent_without_workspace():
    state = NumaxState()
    result = OperatorSubagent().act(state)

    assert result["decision"] == "open_workspace"
