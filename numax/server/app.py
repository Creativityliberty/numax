from __future__ import annotations

from fastapi import FastAPI

from numax.server.routes.models import router as models_router
from numax.server.routes.providers import router as providers_router
from numax.server.routes.recipes import router as recipes_router
from numax.server.routes.sessions import router as sessions_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="NUMAX Server",
        version="0.1.0",
        description="NUMAX server-first API",
    )

    app.include_router(models_router, prefix="/models", tags=["models"])
    app.include_router(providers_router, prefix="/providers", tags=["providers"])
    app.include_router(recipes_router, prefix="/recipes", tags=["recipes"])
    app.include_router(sessions_router, prefix="/sessions", tags=["sessions"])

    @app.get("/health")
    def health() -> dict:
        return {"ok": True, "service": "numax-server"}

    return app


app = create_app()
