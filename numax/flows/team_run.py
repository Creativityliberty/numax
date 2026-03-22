from numax.core.graph import NumaxGraph
from numax.teams.nodes import TeamLoadNode, TeamMissionNode, TeamResultNode


def build_team_run_flow() -> NumaxGraph:
    graph = NumaxGraph(name="team_run")

    load_node = TeamLoadNode()
    mission_node = TeamMissionNode()
    result_node = TeamResultNode()

    graph.add_node(load_node)
    graph.add_node(mission_node)
    graph.add_node(result_node)

    graph.add_edge("team_load", "mission", "team_mission")
    graph.add_edge("team_mission", "result", "team_result")
    graph.add_edge("team_result", "done", None)

    return graph
