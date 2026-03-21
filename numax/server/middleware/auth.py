from __future__ import annotations

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class SimpleAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user_id = request.headers.get("x-numax-user-id", "local-admin")
        roles_header = request.headers.get("x-numax-roles", "admin")
        roles = [role.strip() for role in roles_header.split(",") if role.strip()]

        request.state.auth = {
            "user_id": user_id,
            "roles": roles,
        }
        return await call_next(request)
