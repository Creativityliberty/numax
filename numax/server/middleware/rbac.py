from __future__ import annotations

from fastapi import HTTPException, Request

from numax.rbac.checks import has_permission


def require_permission(request: Request, permission: str) -> None:
    auth = getattr(request.state, "auth", None) or {}
    roles = auth.get("roles", [])
    if not has_permission(roles, permission):
        raise HTTPException(status_code=403, detail=f"Missing permission: {permission}")
