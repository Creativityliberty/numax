from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from numax.core.state import NumaxState


class BaseSubagent(ABC):
    name: str = "base_subagent"
    role: str = "generic"

    @abstractmethod
    def act(self, state: NumaxState) -> Dict[str, Any]:
        pass
