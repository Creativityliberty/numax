from numax.core.graph import NumaxGraph
from numax.profiles.nodes import ProfileApplyNode


def build_profile_apply_flow() -> NumaxGraph:
    graph = NumaxGraph(name="profile_apply")

    node = ProfileApplyNode()
    graph.add_node(node)
    graph.add_edge("profile_apply", "done", None)

    return graph
