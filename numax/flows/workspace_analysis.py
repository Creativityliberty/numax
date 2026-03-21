from numax.core.graph import NumaxGraph
from numax.workspace.nodes import WorkspaceOpenNode, WorkspaceIndexNode, WorkspaceSummarizeNode


def build_workspace_analysis_flow() -> NumaxGraph:
    graph = NumaxGraph(name="workspace_analysis")

    open_node = WorkspaceOpenNode()
    index_node = WorkspaceIndexNode()
    summarize_node = WorkspaceSummarizeNode()

    graph.add_node(open_node)
    graph.add_node(index_node)
    graph.add_node(summarize_node)

    graph.add_edge("workspace_open", "indexed", "workspace_index")
    graph.add_edge("workspace_index", "summarize", "workspace_summarize")
    graph.add_edge("workspace_summarize", "done", None)

    return graph
