from numax.core.graph import NumaxGraph
from numax.workspace.nodes import WorkspaceOpenNode
from numax.workspace.tool_nodes import WorkspaceSearchNode


def build_workspace_search_flow() -> NumaxGraph:
    graph = NumaxGraph(name="workspace_search")

    open_node = WorkspaceOpenNode()
    search_node = WorkspaceSearchNode()

    graph.add_node(open_node)
    graph.add_node(search_node)

    graph.add_edge("workspace_open", "indexed", "workspace_search")
    graph.add_edge("workspace_search", "done", None)

    return graph
