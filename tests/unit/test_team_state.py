from numax.teams.team_state import TeamState


def test_team_state_defaults():
    state = TeamState(team_id="engineering_squad")
    assert state.status == "idle"
