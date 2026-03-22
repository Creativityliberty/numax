from __future__ import annotations

import uuid

from numax.director.specs import DirectedMission, DirectorPlan


def build_director_plan(objective: str) -> DirectorPlan:
    lowered = objective.lower()

    missions = [
        DirectedMission(
            mission_id=str(uuid.uuid4()),
            team_id="product_squad",
            title="Clarify and structure objective",
            objective=objective,
            expected_outputs=["spec"],
        ),
        DirectedMission(
            mission_id=str(uuid.uuid4()),
            team_id="engineering_squad",
            title="Implement or prepare execution",
            objective=objective,
            expected_outputs=["patch", "implementation_result"],
        ),
        DirectedMission(
            mission_id=str(uuid.uuid4()),
            team_id="qa_squad",
            title="Validate and review outputs",
            objective=objective,
            expected_outputs=["review", "scorecard"],
        ),
    ]

    if "research" in lowered or "citation" in lowered or "survey" in lowered:
        missions.insert(
            1,
            DirectedMission(
                mission_id=str(uuid.uuid4()),
                team_id="research_squad",
                title="Research and evidence gathering",
                objective=objective,
                expected_outputs=["research_notes", "sources"],
            ),
        )

    return DirectorPlan(objective=objective, missions=missions)
