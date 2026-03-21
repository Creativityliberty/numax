from __future__ import annotations

from typing import Any, Dict

from numax.obs.otel_exporter import DummyOTelExporter


EXPORTER = DummyOTelExporter()


def export_span_record(record: Dict[str, Any]) -> Dict[str, Any]:
    return EXPORTER.export_span(record)
