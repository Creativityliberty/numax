from numax.core.graph import NumaxGraph
from numax.critic.basic import BasicCriticNode
from numax.reason.answer import AnswerNode
from numax.retrieve.node import RetrieveNode
from numax.router.intent import IntentRouterNode


def build_retrieval_answer_flow() -> NumaxGraph:
    graph = NumaxGraph(name="retrieval_answer")

    router = IntentRouterNode()
    retrieve = RetrieveNode()
    answer = AnswerNode()
    critic = BasicCriticNode()

    graph.add_node(router)
    graph.add_node(retrieve)
    graph.add_node(answer)
    graph.add_node(critic)

    graph.add_edge("intent_router", "retrieve", "retrieve")
    graph.add_edge("intent_router", "answer", "answer")
    graph.add_edge("retrieve", "answer", "answer")
    graph.add_edge("answer", "critic", "basic_critic")
    graph.add_edge("basic_critic", "done", None)
    graph.add_edge("basic_critic", "halt", None)

    return graph
