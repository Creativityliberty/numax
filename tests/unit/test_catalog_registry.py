from numax.catalog.registry import build_catalog_registry


def test_catalog_registry_builds():
    registry = build_catalog_registry()
    assert len(registry["items"]) >= 1
