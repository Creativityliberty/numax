from numax.core.graph import NumaxGraph
from numax.specs.nodes import IntentSpecNode, SpecValidationNode


def build_specification_loop_flow() -> NumaxGraph:
    graph = NumaxGraph(name="specification_loop")

    intent_node = IntentSpecNode()
    validation_node = SpecValidationNode()

    graph.add_node(intent_node)
    graph.add_node(validation_node)

    graph.add_edge("intent_spec", "validate", "spec_validation")
    graph.add_edge("spec_validation", "done", None)

    return graph
