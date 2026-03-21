from __future__ import annotations

from pydantic import BaseModel, Field

from numax.models.catalog import ModelCatalog, ModelSpec


class RuntimePolicy(BaseModel):
    preferred: dict[str, str] = Field(default_factory=dict)
    fallbacks: dict[str, list[str]] = Field(default_factory=dict)


class ModelResolver:
    def __init__(self, catalog: ModelCatalog, policy: RuntimePolicy) -> None:
        self.catalog = catalog
        self.policy = policy

    def resolve(self, role: str) -> ModelSpec:
        preferred_id = self.policy.preferred.get(role)
        if preferred_id:
            spec = self.catalog.get(preferred_id)
            if spec.status == "enabled":
                return spec

        for fallback_id in self.policy.fallbacks.get(role, []):
            spec = self.catalog.get(fallback_id)
            if spec.status == "enabled":
                return spec

        role_candidates = self.catalog.list_by_role(role)
        if role_candidates:
            return role_candidates[0]

        raise LookupError(f"No enabled model available for role '{role}'.")
