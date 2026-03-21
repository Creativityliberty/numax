from numax.core.graph import NumaxGraph
from numax.learning.nodes import LearningFeedbackNode, LearningRecommendNode


def build_learning_feedback_flow() -> NumaxGraph:
    graph = NumaxGraph(name="learning_feedback_loop")

    feedback_node = LearningFeedbackNode()
    recommend_node = LearningRecommendNode()

    graph.add_node(feedback_node)
    graph.add_node(recommend_node)

    graph.add_edge("learning_feedback", "done", "learning_recommend")
    graph.add_edge("learning_recommend", "done", None)

    return graph
