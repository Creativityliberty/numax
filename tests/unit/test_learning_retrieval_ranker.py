from numax.learning.retrieval_ranker import rerank_results


def test_rerank_results_keeps_best_first():
    rows = [
        {"source_id": "a", "text": "A", "score": 1.0},
        {"source_id": "b", "text": "B", "score": 2.0},
    ]

    ranked = rerank_results(rows)

    assert ranked[0]["source_id"] == "b"
    assert ranked[1]["source_id"] == "a"
