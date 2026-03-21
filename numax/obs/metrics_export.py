from __future__ import annotations

import json
from pathlib import Path
from typing import Any

METRICS_PATH = Path("data/traces/metrics.jsonl")
METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)


def emit_metric(name: str, value: float, **labels: Any) -> None:
    record = {
        "metric": name,
        "value": value,
        "labels": labels,
    }
    with METRICS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
