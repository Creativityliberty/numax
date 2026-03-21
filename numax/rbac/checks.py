from __future__ import annotations

from collections.abc import Iterable

from numax.rbac.policies import ROLE_PERMISSIONS


def collect_permissions(roles: Iterable[str]) -> set[str]:
    permissions: set[str] = set()
    for role in roles:
        permissions.update(ROLE_PERMISSIONS.get(role, []))
    return permissions


def has_permission(roles: Iterable[str], permission: str) -> bool:
    return permission in collect_permissions(roles)
