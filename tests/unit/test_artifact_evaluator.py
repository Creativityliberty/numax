from numax.artifacts.evaluators import evaluate_artifact


def test_evaluate_artifact_returns_scores():
    result = evaluate_artifact({"text": "hello world from numax artifact", "trace": [1]})
    assert result["overall"] > 0.0
