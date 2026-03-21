from numax.core.state import NumaxState
from numax.subagents.reviewer import ReviewerSubagent


def test_reviewer_subagent_with_review():
    state = NumaxState()
    state.world_state["code_review"] = {
        "decision": "accept",
        "risk": "low",
        "scope": "narrow",
        "notes": ["Tests passed."],
    }

    result = ReviewerSubagent().act(state)
    assert result["recommendation"] == "accept"
