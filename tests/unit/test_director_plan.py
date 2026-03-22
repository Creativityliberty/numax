from numax.director.planner import build_director_plan


def test_build_director_plan():
    plan = build_director_plan("Implement NUMAX V3")
    assert len(plan.missions) >= 3
