from numax.bootstrap import build_model_catalog, build_model_resolver

def test_model_resolver_returns_default_config_model():
    catalog = build_model_catalog()
    resolver = build_model_resolver(catalog)

    spec = resolver.resolve("primary")

    # In default config (mock enabled), mock-large is the primary fallback
    assert spec.id == "mock:mock-large"
    assert spec.provider == "mock"
