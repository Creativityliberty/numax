from __future__ import annotations

from fastapi import APIRouter, Request

from numax.server.middleware.rbac import require_permission

router = APIRouter()


@router.get("/whoami")
def whoami(request: Request) -> dict:
    return getattr(request.state, "auth", {})


@router.get("/permissions-check")
def permissions_check(request: Request, permission: str) -> dict:
    require_permission(request, permission)
    return {"ok": True, "permission": permission}
