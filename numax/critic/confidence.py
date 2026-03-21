from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ConfidenceThresholds:
    min_execution: float = 0.6
    min_validation: float = 0.8
    min_safety: float = 0.6


def aggregate_confidence(state) -> float:
    values = [
        state.confidence.understanding_confidence,
        state.confidence.output_confidence,
        state.confidence.safety_confidence,
    ]

    if state.retrieved_context:
        values.append(state.confidence.source_confidence)

    return min(values) if values else 0.0


def can_execute(state, thresholds: ConfidenceThresholds | None = None) -> bool:
    thresholds = thresholds or ConfidenceThresholds()
    global_conf = aggregate_confidence(state)

    if state.confidence.safety_confidence < thresholds.min_safety:
        return False

    return global_conf >= thresholds.min_execution


def can_validate(state, thresholds: ConfidenceThresholds | None = None) -> bool:
    thresholds = thresholds or ConfidenceThresholds()
    return aggregate_confidence(state) >= thresholds.min_validation
