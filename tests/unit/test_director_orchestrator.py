from numax.director.orchestrator import DirectorOrchestrator
from numax.director.planner import build_director_plan


def test_director_assign():
    plan = build_director_plan("Implement NUMAX V3")
    assignments = DirectorOrchestrator().assign(plan)
    assert len(assignments) == len(plan.missions)
