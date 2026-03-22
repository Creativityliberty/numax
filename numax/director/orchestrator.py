from __future__ import annotations

from typing import Any, Dict, List

from numax.director.specs import DirectorAssignment, DirectorPlan


class DirectorOrchestrator:
    def assign(self, plan: DirectorPlan) -> List[DirectorAssignment]:
        assignments: List[DirectorAssignment] = []

        for mission in plan.missions:
            assignments.append(
                DirectorAssignment(
                    team_id=mission.team_id,
                    mission_id=mission.mission_id,
                    accepted=True,
                    notes=[f"Mission assigned to {mission.team_id}."],
                )
            )

        return assignments

    def consolidate(self, plan: DirectorPlan, team_results: Dict[str, Any]) -> Dict[str, Any]:
        consolidated = {
            "objective": plan.objective,
            "mission_count": len(plan.missions),
            "teams_involved": [mission.team_id for mission in plan.missions],
            "team_results": team_results,
            "status": "partial" if not team_results else "consolidated",
        }

        if all(team in team_results for team in consolidated["teams_involved"]):
            consolidated["status"] = "complete"

        return consolidated
