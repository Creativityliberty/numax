from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AuthContext:
    user_id: str
    roles: list[str]
    email: str | None = None


def build_local_admin_context() -> AuthContext:
    return AuthContext(
        user_id="local-admin",
        roles=["admin"],
        email=None,
    )
