from __future__ import annotations

ROLE_PERMISSIONS: dict[str, list[str]] = {
    "admin": [
        "skills.apply",
        "skills.uninstall",
        "skills.replay",
        "jobs.create",
        "jobs.run",
        "jobs.read",
        "sessions.read",
        "providers.use",
        "sandbox.exec",
        "server.admin",
    ],
    "builder": [
        "skills.apply",
        "skills.replay",
        "jobs.create",
        "jobs.run",
        "providers.use",
        "sandbox.exec",
    ],
    "operator": [
        "jobs.create",
        "jobs.run",
        "providers.use",
    ],
    "viewer": [
        "jobs.read",
        "sessions.read",
    ],
}
