from __future__ import annotations

ALLOWED_COMMANDS = {
    "python",
    "python3",
    "pytest",
    "echo",
    "ls",
    "cat",
}

BLOCKED_TOKENS = {
    "rm",
    "shutdown",
    "reboot",
    "mkfs",
    "dd",
}
