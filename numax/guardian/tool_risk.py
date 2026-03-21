from __future__ import annotations

from typing import Literal

RiskLevel = Literal["low", "medium", "high"]


def classify_tool_risk(tool_name: str) -> RiskLevel:
    if tool_name in {"shell", "exec", "python_exec"}:
        return "high"
    if tool_name in {"search", "retrieve"}:
        return "medium"
    return "low"
