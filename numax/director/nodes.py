from __future__ import annotations

from typing import Any, Dict

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.director.orchestrator import DirectorOrchestrator
from numax.director.planner import build_director_plan
from numax.director.specs import DirectorPlan
from numax.flows.team_map_reduce import run_team_map_reduce


class DirectorPlanNode(NumaxNode):
    name = "director_plan"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "objective": state.observation.get("raw_input", ""),
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        plan = build_director_plan(payload["objective"])
        return {"plan": plan.model_dump()}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        state.director_plan = result["plan"]
        state.add_trace(self.name, "post", "Director plan created", mission_count=len(result["plan"]["missions"]))
        return "assign"


class DirectorAssignNode(NumaxNode):
    name = "director_assign"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "plan": state.director_plan,
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        orchestrator = DirectorOrchestrator()
        assignments = orchestrator.assign(DirectorPlan(**payload["plan"]))
        return {"assignments": [item.model_dump() for item in assignments]}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        state.director_assignments = result["assignments"]
        state.add_trace(self.name, "post", "Director assignments created", count=len(result["assignments"]))
        return "run"


class DirectorRunTeamsNode(NumaxNode):
    name = "director_run_teams"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        plan = state.director_plan or {}
        missions = plan.get("missions", [])
        return {
            "missions": [
                {
                    "team_id": mission["team_id"],
                    "raw_input": mission["objective"],
                }
                for mission in missions
            ]
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        base_state = NumaxState()
        result = run_team_map_reduce(base_state=base_state, missions=payload["missions"])
        return {"map_reduce_result": result}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        state.map_reduce_result = result["map_reduce_result"]
        state.team_results = {
            item["observation"]["team_id"]: item["team_results"].get(item["observation"]["team_id"])
            for item in result["map_reduce_result"]["results"]
            if item.get("team_results")
        }
        state.add_trace(self.name, "post", "Director executed team map-reduce")
        return "consolidate"


class DirectorConsolidateNode(NumaxNode):
    name = "director_consolidate"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "plan": state.director_plan,
            "team_results": state.team_results,
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        orchestrator = DirectorOrchestrator()
        consolidated = orchestrator.consolidate(
            plan=DirectorPlan(**payload["plan"]),
            team_results=payload["team_results"],
        )
        return {"director_result": consolidated}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        state.director_results = result["director_result"]
        state.final_output = result["director_result"]
        state.next_recommended_action = "publish_director_result"
        state.add_trace(
            self.name,
            "post",
            "Director consolidated results",
            status=result["director_result"]["status"],
        )
        return "done"
