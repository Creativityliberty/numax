from __future__ import annotations

import uuid
from typing import Any, Dict

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.teams.handover import validate_handover
from numax.teams.registry import build_default_team_registry
from numax.teams.specs import TeamMission
from numax.teams.team_state import TeamState


class TeamLoadNode(NumaxNode):
    name = "team_load"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "team_id": state.observation.get("team_id", "product_squad"),
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        registry = build_default_team_registry()
        team = registry.get(payload["team_id"])
        return {"team": team.model_dump()}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        team = result["team"]
        state.teams_state[team["team_id"]] = TeamState(team_id=team["team_id"], status="ready").model_dump()
        state.add_trace(self.name, "post", "Team loaded", team_id=team["team_id"])
        return "mission"


class TeamMissionNode(NumaxNode):
    name = "team_mission"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        team_id = state.observation.get("team_id", "product_squad")
        return {
            "team_id": team_id,
            "raw_input": state.observation.get("raw_input", ""),
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        mission = TeamMission(
            mission_id=str(uuid.uuid4()),
            title=f"Mission for {payload['team_id']}",
            objective=payload["raw_input"] or f"Default mission for {payload['team_id']}",
            inputs={},
            expected_outputs=["team_result"],
            constraints=[],
            priority=5,
        )
        return {"mission": mission.model_dump()}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        team_id = payload["team_id"]
        current = TeamState(**state.teams_state[team_id])
        current.active_mission = TeamMission(**result["mission"])
        current.status = "running"
        current.notes.append("Mission assigned.")
        state.teams_state[team_id] = current.model_dump()
        state.add_trace(self.name, "post", "Team mission assigned", team_id=team_id)
        return "result"


class TeamResultNode(NumaxNode):
    name = "team_result"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        team_id = state.observation.get("team_id", "product_squad")
        return {
            "team_id": team_id,
            "team_state": state.teams_state.get(team_id, {}),
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        team_state = TeamState(**payload["team_state"])
        mission = team_state.active_mission

        artifact = {
            "team_id": payload["team_id"],
            "mission_id": mission.mission_id if mission else None,
            "objective": mission.objective if mission else None,
            "result": f"Consolidated output from {payload['team_id']}",
        }

        return {"artifact": artifact}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        team_id = payload["team_id"]
        current = TeamState(**state.teams_state[team_id])
        current.produced_artifacts.append(result["artifact"])
        current.status = "done"
        current.notes.append("Mission completed.")
        state.teams_state[team_id] = current.model_dump()

        state.team_results[team_id] = result["artifact"]
        state.next_recommended_action = "handover_or_next_team"

        state.add_trace(self.name, "post", "Team result produced", team_id=team_id)
        return "done"


class TeamHandoverNode(NumaxNode):
    name = "team_handover"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "from_team": state.observation.get("from_team", "product_squad"),
            "to_team": state.observation.get("to_team", "engineering_squad"),
            "artifact_type": state.observation.get("artifact_type", "spec"),
            "payload": state.observation.get("handover_payload", {}),
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        record = validate_handover(
            from_team=payload["from_team"],
            to_team=payload["to_team"],
            artifact_type=payload["artifact_type"],
            payload=payload["payload"],
        )
        return {"handover": record.model_dump()}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        record = result["handover"]
        state.handover_log.append(record)
        state.next_recommended_action = "accept_handover" if record["accepted"] else "repair_handover"
        state.add_trace(
            self.name,
            "post",
            "Team handover validated",
            from_team=record["from_team"],
            to_team=record["to_team"],
            accepted=record["accepted"],
        )
        return "done"
