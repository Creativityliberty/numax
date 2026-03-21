from __future__ import annotations

from typing import Any

from numax.core.node import NumaxNode
from numax.core.state import CritiqueState, NumaxState
from numax.critic.confidence import aggregate_confidence
from numax.learning.critic_calibration import calibrate_confidence


class BasicCriticNode(NumaxNode):
    name = "basic_critic"

    def prep(self, state: NumaxState) -> dict[str, Any]:
        payload = {
            "candidate_output": state.candidate_output,
            "safety_confidence": state.confidence.safety_confidence,
            "aggregated_confidence": aggregate_confidence(state),
        }
        state.add_trace(self.name, "prep", "Critic payload prepared")
        return payload

    def exec(self, payload: dict[str, Any]) -> dict[str, Any]:
        notes = []
        ok = True

        if payload["candidate_output"] is None:
            ok = False
            notes.append("No candidate output produced.")

        if payload["safety_confidence"] < 0.6:
            ok = False
            notes.append("Safety confidence too low.")

        if payload["aggregated_confidence"] < 0.5:
            notes.append("Low aggregate confidence.")

        raw_confidence = 0.85 if ok else 0.30
        confidence = calibrate_confidence(raw_confidence)

        return {
            "ok": ok,
            "notes": notes,
            "confidence": confidence,
        }

    def post(
        self,
        state: NumaxState,
        payload: dict[str, Any],
        result: dict[str, Any],
    ) -> str:
        state.critique = CritiqueState(
            ok=result["ok"],
            notes=result["notes"],
            confidence=result["confidence"],
        )

        if result["ok"]:
            state.final_output = state.candidate_output
            state.runtime.fsm_state = "LEARN"
            return "done"

        state.runtime.degraded = True
        state.runtime.fsm_state = "DEGRADED"
        return "halt"
