from numax.core.graph import NumaxGraph
from numax.teams.blackboard_nodes import BlackboardPublishNode, BlackboardConsumeNode


def build_blackboard_cycle_flow() -> NumaxGraph:
    graph = NumaxGraph(name="blackboard_cycle")

    publish_node = BlackboardPublishNode()
    consume_node = BlackboardConsumeNode()

    graph.add_node(publish_node)
    graph.add_node(consume_node)

    graph.add_edge("blackboard_publish", "consume", "blackboard_consume")
    graph.add_edge("blackboard_consume", "done", None)

    return graph
