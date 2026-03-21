from __future__ import annotations

from typing import Any

from numax.obs.spans import Span, SpanManager

SPAN_MANAGER = SpanManager()


def start_runtime_span(
    name: str,
    trace_id: str,
    parent_span_id: str | None = None,
    **attrs: Any,
) -> Span:
    return SPAN_MANAGER.start_span(
        name=name,
        trace_id=trace_id,
        parent_span_id=parent_span_id,
        attributes=attrs,
    )
