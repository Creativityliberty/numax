from numax.catalog.nodes import CatalogSyncNode
from numax.core.graph import NumaxGraph


def build_catalog_sync_flow() -> NumaxGraph:
    graph = NumaxGraph(name="catalog_sync")
    node = CatalogSyncNode()
    graph.add_node(node)
    graph.add_edge("catalog_sync", "done", None)
    return graph
