from numax.sandbox.runtime_isolation import run_isolated_command
from numax.sandbox.specs import SandboxCommand


def test_sandbox_echo_allowed() -> None:
    result = run_isolated_command(SandboxCommand(command=["echo", "hello"]))
    assert result["ok"] is True
    assert "hello" in result["stdout"]
