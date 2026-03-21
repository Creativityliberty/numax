import os
from unittest.mock import patch
from numax.bootstrap import build_model_catalog, build_model_resolver


@patch.dict(os.environ, {"GOOGLE_API_KEY": ""}, clear=True)
def test_model_resolver_returns_mock_when_no_key():
    catalog = build_model_catalog()
    resolver = build_model_resolver(catalog)

    spec = resolver.resolve("primary")

    assert spec.id == "mock:mock-large"
    assert spec.provider == "mock"
    assert spec.model_name == "mock-large"


@patch.dict(os.environ, {"GOOGLE_API_KEY": "fake_key"})
def test_model_resolver_returns_google_when_key_exists():
    catalog = build_model_catalog()
    resolver = build_model_resolver(catalog)

    spec = resolver.resolve("primary")

    assert spec.id == "google:gemini-3.1-pro-preview"
    assert spec.provider == "google"
    assert spec.model_name == "gemini-3.1-pro-preview"

