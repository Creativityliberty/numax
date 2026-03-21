from numax.core.graph import NumaxGraph
from numax.core.node import NumaxNode
from numax.core.state import NumaxState


class DummyNode(NumaxNode):
    name = "dummy"

    def exec(self, payload):
        return {"ok": True}

    def post(self, state, payload, result):
        state.world_state["dummy_ran"] = True
        return "done"


def test_graph_runs_node_and_stops():
    graph = NumaxGraph(name="test_graph")
    graph.add_node(DummyNode())
    graph.add_edge("dummy", "done", None)

    state = NumaxState()
    final_state = graph.run(start="dummy", state=state)

    assert final_state.world_state["dummy_ran"] is True
    assert final_state.runtime.flow_name == "test_graph"
