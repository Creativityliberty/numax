from __future__ import annotations

from fastapi import FastAPI

from numax.server.middleware.auth import SimpleAuthMiddleware
from numax.server.routes import (
    admin,
    async_models,
    jobs,
    models,
    providers,
    recipes,
    sandbox,
    sessions,
)


def create_app() -> FastAPI:
    app = FastAPI(
        title="NUMAX Server",
        version="0.1.0",
        description="NUMAX server-first API",
    )
    app.add_middleware(SimpleAuthMiddleware)

    app.include_router(models.router, prefix="/models", tags=["models"])
    app.include_router(providers.router, prefix="/providers", tags=["providers"])
    app.include_router(recipes.router, prefix="/recipes", tags=["recipes"])
    app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
    app.include_router(async_models.router, prefix="/async", tags=["async"])
    app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
    app.include_router(admin.router, prefix="/admin", tags=["admin"])
    app.include_router(sandbox.router, prefix="/sandbox", tags=["sandbox"])

    @app.get("/health")
    def health() -> dict:
        return {"ok": True, "service": "numax-server"}

    return app


app = create_app()
