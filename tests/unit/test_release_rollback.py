from numax.release.rollback import rollback_to


def test_rollback_returns_restored_skills():
    result = rollback_to("last_known_good")

    assert result.ok is True
    assert isinstance(result.restored_skills, list)
