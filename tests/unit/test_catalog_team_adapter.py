from numax.catalog.team_adapter import skill_to_team_template


def test_skill_to_team_template():
    result = skill_to_team_template(
        {
            "skill_id": "skill-architect",
            "title": "Skill Architect",
            "description": "Audit skills",
        }
    )
    assert result is not None
    assert result["team_id"] == "audit_squad"
