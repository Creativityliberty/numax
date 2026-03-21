from numax.core.graph import NumaxGraph
from numax.improve.nodes import ImprovementLoopNode


def build_improvement_loop_flow() -> NumaxGraph:
    graph = NumaxGraph(name="improvement_loop")

    node = ImprovementLoopNode()
    graph.add_node(node)
    graph.add_edge("improvement_loop", "done", None)

    return graph
