from numax.core.state import NumaxState
from numax.critic.confidence import aggregate_confidence, can_execute


def test_aggregate_confidence_uses_minimum():
    state = NumaxState()
    state.confidence.understanding_confidence = 0.9
    state.confidence.output_confidence = 0.7
    state.confidence.safety_confidence = 0.8

    assert aggregate_confidence(state) == 0.7


def test_can_execute_false_if_safety_too_low():
    state = NumaxState()
    state.confidence.understanding_confidence = 0.9
    state.confidence.output_confidence = 0.9
    state.confidence.safety_confidence = 0.2

    assert can_execute(state) is False
