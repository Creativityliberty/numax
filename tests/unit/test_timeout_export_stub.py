from numax.obs.otel_exporter import DummyOTelExporter


def test_dummy_otel_exporter_exports_span():
    exporter = DummyOTelExporter()
    result = exporter.export_span({"name": "x"})
    assert result["ok"] is True
