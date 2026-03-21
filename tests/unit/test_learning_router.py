from numax.learning.router import route_intent_adaptive


def test_route_intent_adaptive_retrieves_on_keyword():
    result = route_intent_adaptive("search NUMAX memory", has_context=False)

    assert result["route"] == "retrieve"
    assert result["understanding_confidence"] >= 0.8


def test_route_intent_adaptive_defaults_to_answer():
    result = route_intent_adaptive("Explain NUMAX simply", has_context=False)

    assert result["route"] == "answer"
