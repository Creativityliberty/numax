from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from numax.core.state import NumaxState


class NumaxNode(ABC):
    name: str = "unnamed"
    max_retries: int = 0

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        """
        Read from state and prepare an execution payload.
        """
        state.add_trace(self.name, "prep", "Preparing payload")
        return {}

    @abstractmethod
    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pure execution step.
        Should not mutate state directly.
        """
        raise NotImplementedError

    def exec_fallback(
        self,
        state: NumaxState,
        payload: Dict[str, Any],
        exc: Exception,
    ) -> Dict[str, Any]:
        """
        Fallback path on execution error.
        Default behavior: re-raise.
        """
        state.add_trace(
            self.name,
            "fallback",
            "Fallback triggered",
            error=str(exc),
        )
        raise exc

    def post(
        self,
        state: NumaxState,
        payload: Dict[str, Any],
        result: Dict[str, Any],
    ) -> str:
        """
        Write execution results to state and return the transition label.
        """
        state.add_trace(self.name, "post", "Post-processing result")
        return "default"

    def run(self, state: NumaxState) -> str:
        payload = self.prep(state)
        try:
            state.add_trace(self.name, "exec", "Executing node", payload=payload)
            result = self.exec(payload)
        except Exception as exc:
            state.add_trace(self.name, "error", "Execution failed", error=str(exc))
            result = self.exec_fallback(state, payload, exc)

        transition = self.post(state, payload, result)
        state.add_trace(
            self.name,
            "transition",
            "Transition selected",
            transition=transition,
        )
        return transition
