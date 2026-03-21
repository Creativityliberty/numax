from __future__ import annotations


def build_otel_resource(service_name: str = "numax", service_version: str = "v1") -> dict:
    return {
        "service.name": service_name,
        "service.version": service_version,
    }
