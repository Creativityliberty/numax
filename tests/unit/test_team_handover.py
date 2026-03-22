from numax.teams.handover import validate_handover


def test_validate_spec_handover_ok():
    record = validate_handover(
        from_team="product_squad",
        to_team="engineering_squad",
        artifact_type="spec",
        payload={"objective": "Implement feature X"},
    )

    assert record.accepted is True
