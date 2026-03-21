from numax.skills.apply import apply_skill
from numax.skills.runtime_overrides import load_runtime_overrides
from numax.skills.uninstall import uninstall_skill


def test_uninstall_skill_reverts_runtime_override() -> None:
    apply_skill("memory_plus", preview=False)
    assert load_runtime_overrides()["runtime"]["max_retries"] == 3

    result = uninstall_skill("memory_plus")
    assert result.ok is True
