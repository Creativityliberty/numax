from numax.improve.mutation_gate import evaluate_mutation_gate


def test_mutation_gate_blocks_when_degraded():
    result = evaluate_mutation_gate(
        suggestions=[{"type": "revise_patch", "priority": "high"}],
        safety_confidence=1.0,
        degraded=True,
    )

    assert result["allowed"] is False
