from numax.core.graph import NumaxGraph
from numax.runtime.nodes import (
    RuntimeCollectEventsNode,
    RuntimeBufferEventsNode,
    RuntimeTimeoutPolicyNode,
)


def build_runtime_resilience_flow() -> NumaxGraph:
    graph = NumaxGraph(name="runtime_resilience")

    collect_node = RuntimeCollectEventsNode()
    buffer_node = RuntimeBufferEventsNode()
    timeout_node = RuntimeTimeoutPolicyNode()

    graph.add_node(collect_node)
    graph.add_node(buffer_node)
    graph.add_node(timeout_node)

    graph.add_edge("runtime_collect_events", "buffer", "runtime_buffer_events")
    graph.add_edge("runtime_buffer_events", "timeout", "runtime_timeout_policy")
    graph.add_edge("runtime_timeout_policy", "done", None)

    return graph
