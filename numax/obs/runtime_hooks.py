from __future__ import annotations

from numax.obs.metrics_export import emit_metric
from numax.obs.otel import start_runtime_span
from numax.obs.spans import Span


class RuntimeHookContext:
    def __init__(self, trace_id: str, run_id: str | None = None) -> None:
        self.trace_id = trace_id
        self.run_id = run_id


def instrument_flow_start(flow_name: str, trace_id: str, run_id: str | None = None) -> Span:
    span = start_runtime_span("flow.start", trace_id, flow_name=flow_name, run_id=run_id)
    span.add_event("flow_started", flow_name=flow_name)
    emit_metric("numax.flow.started", 1.0, flow_name=flow_name)
    return span


def instrument_flow_end(flow_name: str, trace_id: str, ok: bool, run_id: str | None = None) -> None:
    span = start_runtime_span("flow.end", trace_id, flow_name=flow_name, run_id=run_id, ok=ok)
    span.add_event("flow_finished", ok=ok)
    span.finish()
    emit_metric("numax.flow.finished", 1.0, flow_name=flow_name, ok=ok)
