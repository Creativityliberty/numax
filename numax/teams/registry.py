from __future__ import annotations

from typing import Dict

from numax.teams.specs import TeamSpec
from numax.teams.templates import (
    build_engineering_squad,
    build_product_squad,
    build_qa_squad,
)


class TeamRegistry:
    def __init__(self) -> None:
        self._teams: Dict[str, TeamSpec] = {}

    def register(self, team: TeamSpec) -> None:
        self._teams[team.team_id] = team

    def get(self, team_id: str) -> TeamSpec:
        if team_id not in self._teams:
            raise KeyError(f"Unknown team: {team_id}")
        return self._teams[team_id]

    def list_ids(self) -> list[str]:
        return sorted(self._teams.keys())


def build_default_team_registry() -> TeamRegistry:
    registry = TeamRegistry()
    registry.register(build_product_squad())
    registry.register(build_engineering_squad())
    registry.register(build_qa_squad())
    return registry
