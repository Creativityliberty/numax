from numax.skills.journal import append_entry, current_installed_skills


def test_skills_journal_tracks_apply_and_uninstall():
    append_entry({"action": "apply", "skill_id": "alpha"})
    assert "alpha" in current_installed_skills()

    append_entry({"action": "uninstall", "skill_id": "alpha"})
    assert "alpha" not in current_installed_skills()
