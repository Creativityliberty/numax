from numax.core.graph import NumaxGraph
from numax.router.intent import IntentRouterNode
from numax.planner.task import PlannerNode
from numax.retrieve.node import RetrieveNode
from numax.reason.answer import AnswerNode
from numax.critic.basic import BasicCriticNode


def build_planning_execution_flow() -> NumaxGraph:
    graph = NumaxGraph(name="planning_execution")

    router = IntentRouterNode()
    planner = PlannerNode()
    retrieve = RetrieveNode()
    answer = AnswerNode()
    critic = BasicCriticNode()

    graph.add_node(router)
    graph.add_node(planner)
    graph.add_node(retrieve)
    graph.add_node(answer)
    graph.add_node(critic)

    graph.add_edge("intent_router", "retrieve", "planner")
    graph.add_edge("intent_router", "answer", "planner")

    graph.add_edge("planner", "retrieve", "retrieve")
    graph.add_edge("planner", "answer", "answer")

    graph.add_edge("retrieve", "answer", "answer")
    graph.add_edge("answer", "critic", "basic_critic")
    graph.add_edge("basic_critic", "done", None)
    graph.add_edge("basic_critic", "halt", None)

    return graph
