from numax.action.artifacts import ArtifactNode
from numax.core.graph import NumaxGraph
from numax.critic.basic import BasicCriticNode
from numax.reason.answer import AnswerNode
from numax.router.intent import IntentRouterNode


def build_artifact_output_flow() -> NumaxGraph:
    graph = NumaxGraph(name="artifact_output")

    router = IntentRouterNode()
    answer = AnswerNode()
    critic = BasicCriticNode()
    artifact = ArtifactNode()

    graph.add_node(router)
    graph.add_node(answer)
    graph.add_node(critic)
    graph.add_node(artifact)

    graph.add_edge("intent_router", "answer", "answer")
    # v0.1 simple flow mapping retrieve directly to answer for now
    graph.add_edge("intent_router", "retrieve", "answer")
    graph.add_edge("answer", "critic", "basic_critic")
    graph.add_edge("basic_critic", "done", "artifact")
    graph.add_edge("basic_critic", "halt", None)
    graph.add_edge("artifact", "done", None)

    return graph
