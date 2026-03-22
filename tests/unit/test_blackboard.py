from numax.teams.blackboard import BlackboardEntry, BlackboardState, add_blackboard_entry


def test_add_blackboard_entry():
    state = BlackboardState()
    entry = BlackboardEntry(
        entry_id="1",
        team_id="product_squad",
        artifact_type="spec",
        payload={"objective": "X"},
    )

    add_blackboard_entry(state, entry)
    assert len(state.entries) == 1
