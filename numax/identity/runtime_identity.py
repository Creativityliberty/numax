from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict

from numax.bootstrap import build_model_catalog, build_provider_registry


VERSION_FILE = Path("VERSION")


def read_version() -> str:
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text(encoding="utf-8").strip()
    return "0.0.0-dev"


def build_runtime_identity(autonomy_mode: str = "ASSISTED") -> Dict[str, Any]:
    provider_registry = build_provider_registry()
    model_catalog = build_model_catalog()

    payload = {
        "version": read_version(),
        "autonomy_mode": autonomy_mode,
        "providers": provider_registry.list_providers(),
        "models": sorted(model.id for model in model_catalog.all()),
    }

    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")
    ).hexdigest()

    payload["identity_hash"] = digest
    return payload
