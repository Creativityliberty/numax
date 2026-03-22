from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any, Dict
from numax.obs.span_bridge import export_span_record

SPAN_LOG_PATH = Path("/Volumes/Numtema/numax/data/traces/spans.jsonl")
SPAN_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


class Span:
    def __init__(
        self,
        name: str,
        trace_id: str,
        span_id: str,
        parent_span_id: str | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> None:
        self.name = name
        self.trace_id = trace_id
        self.span_id = span_id
        self.parent_span_id = parent_span_id
        self.attributes = attributes or {}
        self.start_ts = time.time()
        self.end_ts: float | None = None
        self.status = "ok"
        self.events: list[dict] = []

    def add_event(self, name: str, **payload: Any) -> None:
        self.events.append(
            {
                "name": name,
                "ts": time.time(),
                "payload": payload,
            }
        )

    def set_status(self, status: str) -> None:
        self.status = status

    def finish(self) -> dict:
        self.end_ts = time.time()
        record = {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "name": self.name,
            "attributes": self.attributes,
            "status": self.status,
            "events": self.events,
            "start_ts": self.start_ts,
            "end_ts": self.end_ts,
            "duration_ms": (self.end_ts - self.start_ts) * 1000.0,
        }
        with SPAN_LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        export_span_record(record)
        return record


class SpanManager:
    def new_trace_id(self) -> str:
        return uuid.uuid4().hex

    def new_span_id(self) -> str:
        return uuid.uuid4().hex[:16]

    def start_span(
        self,
        name: str,
        trace_id: str,
        parent_span_id: str | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> Span:
        return Span(
            name=name,
            trace_id=trace_id,
            span_id=self.new_span_id(),
            parent_span_id=parent_span_id,
            attributes=attributes,
        )
