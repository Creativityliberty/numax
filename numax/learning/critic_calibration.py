from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CRITIC_CALIBRATION_PATH = Path("data/state/critic_calibration.json")
CRITIC_CALIBRATION_PATH.parent.mkdir(parents=True, exist_ok=True)

DEFAULT_CRITIC_POLICY = {
    "confidence_offset": 0.0,
    "strict_mode": False,
}


def load_critic_policy() -> dict[str, Any]:
    if not CRITIC_CALIBRATION_PATH.exists():
        return dict(DEFAULT_CRITIC_POLICY)
    try:
        data = json.loads(CRITIC_CALIBRATION_PATH.read_text(encoding="utf-8"))
        return {**DEFAULT_CRITIC_POLICY, **(data or {})}
    except Exception:
        return dict(DEFAULT_CRITIC_POLICY)


def save_critic_policy(policy: dict[str, Any]) -> None:
    CRITIC_CALIBRATION_PATH.write_text(json.dumps(policy, indent=2), encoding="utf-8")


def calibrate_confidence(raw_confidence: float) -> float:
    policy = load_critic_policy()
    value = raw_confidence + float(policy.get("confidence_offset", 0.0))
    if policy.get("strict_mode", False):
        value -= 0.05
    return max(0.0, min(1.0, value))
