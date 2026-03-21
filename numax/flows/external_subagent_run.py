from numax.core.graph import NumaxGraph
from numax.subagents.external_nodes import ExternalSubagentNode


def build_external_subagent_run_flow() -> NumaxGraph:
    graph = NumaxGraph(name="external_subagent_run")

    node = ExternalSubagentNode()
    graph.add_node(node)
    graph.add_edge("external_subagent", "done", None)

    return graph
