from numax.learning.policy_feedback import apply_feedback


def test_apply_feedback_returns_dict():
    result = apply_feedback({"target": "router", "add_retrieve_keywords": ["paper"]})

    assert "router" in result
