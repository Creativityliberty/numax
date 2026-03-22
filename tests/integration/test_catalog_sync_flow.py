from numax.core.state import NumaxState
from numax.flows.catalog_sync import build_catalog_sync_flow


def test_catalog_sync_flow():
    state = NumaxState()
    graph = build_catalog_sync_flow()
    final_state = graph.run(start="catalog_sync", state=state)

    assert final_state.catalog_sync_result["item_count"] >= 1
