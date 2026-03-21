from __future__ import annotations

from typing import Any, Dict


class DummyOTelExporter:
    def export_span(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"ok": True, "exported": True, "kind": "span", "payload": payload}

    def export_metric(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"ok": True, "exported": True, "kind": "metric", "payload": payload}
