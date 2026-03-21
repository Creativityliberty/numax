from numax.learning.model_selector import select_model_for_role


def test_select_model_for_primary_role():
    spec = select_model_for_role("primary")

    assert spec["provider"] in {"mock", "openai", "anthropic", "google", "ollama"}
    assert spec["model_name"]
