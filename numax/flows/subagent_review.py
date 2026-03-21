from numax.core.graph import NumaxGraph
from numax.subagents.nodes import SubagentOrchestrateNode


def build_subagent_review_flow() -> NumaxGraph:
    graph = NumaxGraph(name="subagent_review")

    node = SubagentOrchestrateNode()
    graph.add_node(node)
    graph.add_edge("subagent_orchestrate", "done", None)

    return graph
