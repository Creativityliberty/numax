from __future__ import annotations

from pydantic import BaseModel, Field


class ModelSpec(BaseModel):
    id: str
    provider: str
    model_name: str
    roles: list[str] = Field(default_factory=list)
    capabilities: list[str] = Field(default_factory=list)
    supports_json: bool = False
    supports_tools: bool = False
    supports_vision: bool = False
    context_window: int | None = None
    status: str = "enabled"
    pricing: dict[str, float] = Field(default_factory=dict)


class ModelCatalog:
    def __init__(self) -> None:
        self._models: dict[str, ModelSpec] = {}

    def register(self, spec: ModelSpec) -> None:
        if spec.id in self._models:
            raise ValueError(f"Model '{spec.id}' already exists.")
        self._models[spec.id] = spec

    def get(self, model_id: str) -> ModelSpec:
        if model_id not in self._models:
            raise KeyError(f"Unknown model: {model_id}")
        return self._models[model_id]

    def all(self) -> list[ModelSpec]:
        return list(self._models.values())

    def list_enabled(self) -> list[ModelSpec]:
        return [m for m in self._models.values() if m.status == "enabled"]

    def list_by_role(self, role: str) -> list[ModelSpec]:
        return [m for m in self.list_enabled() if role in m.roles]

    def list_by_capability(self, capability: str) -> list[ModelSpec]:
        return [m for m in self.list_enabled() if capability in m.capabilities]
