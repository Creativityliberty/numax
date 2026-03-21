from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml


CONFIG_DIR = Path("configs")


def _read_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data or {}


def _deep_merge(base: Dict[str, Any], extra: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(base)
    for key, value in extra.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config() -> Dict[str, Any]:
    """
    Load NUMAX config from the default config directory.
    Merge order:
    base <- providers <- routing <- budget <- governance
    """
    config = {}

    for filename in [
        "base.yaml",
        "providers.yaml",
        "routing.yaml",
        "budget.yaml",
        "governance.yaml",
    ]:
        config = _deep_merge(config, _read_yaml(CONFIG_DIR / filename))

    return config


def get_runtime_autonomy_mode(config: Dict[str, Any]) -> str:
    return config.get("runtime", {}).get("autonomy_mode", "ASSISTED")


def get_budget_limits(config: Dict[str, Any]) -> Dict[str, Any]:
    budget = config.get("budget", {})
    return {
        "max_tokens_total": budget.get("max_tokens_total", 20000),
        "max_cost_usd": budget.get("max_cost_usd", 1.0),
        "mode": budget.get("mode", "balanced"),
    }


def get_routing_config(config: Dict[str, Any]) -> Dict[str, Any]:
    return config.get("models", {})


def get_provider_config(config: Dict[str, Any]) -> Dict[str, Any]:
    return config.get("providers", {})
