from __future__ import annotations

from typing import Dict

from numax.profiles.specs import RuntimeProfile


class ProfileRegistry:
    def __init__(self) -> None:
        self._profiles: Dict[str, RuntimeProfile] = {}

    def register(self, profile: RuntimeProfile) -> None:
        self._profiles[profile.profile_id] = profile

    def get(self, profile_id: str) -> RuntimeProfile:
        if profile_id not in self._profiles:
            raise KeyError(f"Unknown profile: {profile_id}")
        return self._profiles[profile_id]

    def list_ids(self) -> list[str]:
        return sorted(self._profiles.keys())


def build_default_profile_registry() -> ProfileRegistry:
    registry = ProfileRegistry()

    registry.register(
        RuntimeProfile(
            profile_id="repo_operator",
            title="Repo Operator",
            description="Profile optimized for repo inspection, patching, testing, and review loops.",
            skills=["research_mode", "critic_strict"],
            config_overrides={
                "runtime": {
                    "autonomy_mode": "SEMI_AUTONOMOUS",
                    "max_retries": 3,
                }
            },
            model_preferences={"primary": "mock:mock-small"},
            router_keywords=["bug", "patch", "repo", "test"],
            critic_policy={"strict_mode": True},
        )
    )

    registry.register(
        RuntimeProfile(
            profile_id="research_mode",
            title="Research Mode",
            description="Profile optimized for retrieval, surveying, and evidence-heavy tasks.",
            skills=["research_mode"],
            config_overrides={
                "runtime": {
                    "autonomy_mode": "ASSISTED",
                    "max_retries": 2,
                }
            },
            model_preferences={"primary": "mock:mock-large"},
            router_keywords=["paper", "survey", "reference", "citation", "research"],
            critic_policy={"strict_mode": False},
        )
    )

    registry.register(
        RuntimeProfile(
            profile_id="benchmark_hardening",
            title="Benchmark Hardening",
            description="Profile optimized for stricter review and more conservative runtime behavior.",
            skills=["critic_strict"],
            config_overrides={
                "runtime": {
                    "autonomy_mode": "SUPERVISED",
                    "max_retries": 1,
                }
            },
            model_preferences={"primary": "mock:mock-small"},
            router_keywords=[],
            critic_policy={"strict_mode": True, "confidence_floor": 0.8},
        )
    )

    registry.register(
        RuntimeProfile(
            profile_id="safe_demo_mode",
            title="Safe Demo Mode",
            description="Profile optimized for demonstrations with conservative execution and strong guardrails.",
            skills=[],
            config_overrides={
                "runtime": {
                    "autonomy_mode": "ASSISTED",
                    "max_retries": 1,
                }
            },
            model_preferences={"primary": "mock:mock-small"},
            router_keywords=[],
            critic_policy={"strict_mode": True},
        )
    )

    return registry
