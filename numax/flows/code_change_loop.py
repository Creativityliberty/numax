from numax.core.graph import NumaxGraph
from numax.workspace.nodes import WorkspaceOpenNode
from numax.workspace.tool_nodes import WorkspaceSearchNode
from numax.workspace.change_nodes import (
    WorkspaceTargetSelectNode,
    WorkspaceReadTargetsNode,
    WorkspacePatchProposalNode,
    WorkspacePatchApplyNode,
    WorkspaceRunTestsNode,
)


from numax.workspace.code_critic_nodes import WorkspaceCodeCriticNode


from numax.subagents.nodes import SubagentOrchestrateNode


def build_code_change_loop_flow() -> NumaxGraph:
    graph = NumaxGraph(name="code_change_loop")

    open_node = WorkspaceOpenNode()
    search_node = WorkspaceSearchNode()
    select_node = WorkspaceTargetSelectNode()
    read_node = WorkspaceReadTargetsNode()
    propose_node = WorkspacePatchProposalNode()
    apply_node = WorkspacePatchApplyNode()
    test_node = WorkspaceRunTestsNode()
    critic_node = WorkspaceCodeCriticNode()
    subagent_node = SubagentOrchestrateNode()

    for node in [
        open_node,
        search_node,
        select_node,
        read_node,
        propose_node,
        apply_node,
        test_node,
        critic_node,
        subagent_node,
    ]:
        graph.add_node(node)

    graph.add_edge("workspace_open", "indexed", "workspace_search")
    graph.add_edge("workspace_search", "done", "workspace_target_select")
    graph.add_edge("workspace_target_select", "read", "workspace_read_targets")
    graph.add_edge("workspace_read_targets", "propose", "workspace_patch_proposal")
    graph.add_edge("workspace_patch_proposal", "apply", "workspace_patch_apply")
    graph.add_edge("workspace_patch_apply", "test", "workspace_run_tests")
    graph.add_edge("workspace_run_tests", "done", "workspace_code_critic")
    graph.add_edge("workspace_code_critic", "done", "subagent_orchestrate")
    graph.add_edge("subagent_orchestrate", "done", None)

    return graph
