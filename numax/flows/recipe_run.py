from numax.core.graph import NumaxGraph
from numax.recipes.nodes import RecipeApplyNode


def build_recipe_run_flow() -> NumaxGraph:
    graph = NumaxGraph(name="recipe_run")

    node = RecipeApplyNode()
    graph.add_node(node)
    graph.add_edge("recipe_apply", "done", None)

    return graph
