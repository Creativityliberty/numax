from numax.core.graph import NumaxGraph
from numax.director.nodes import (
    DirectorAssignNode,
    DirectorConsolidateNode,
    DirectorPlanNode,
    DirectorRunTeamsNode,
)


def build_director_orchestration_flow() -> NumaxGraph:
    graph = NumaxGraph(name="director_orchestration")

    plan_node = DirectorPlanNode()
    assign_node = DirectorAssignNode()
    run_node = DirectorRunTeamsNode()
    consolidate_node = DirectorConsolidateNode()

    graph.add_node(plan_node)
    graph.add_node(assign_node)
    graph.add_node(run_node)
    graph.add_node(consolidate_node)

    graph.add_edge("director_plan", "assign", "director_assign")
    graph.add_edge("director_assign", "run", "director_run_teams")
    graph.add_edge("director_run_teams", "consolidate", "director_consolidate")
    graph.add_edge("director_consolidate", "done", None)

    return graph
