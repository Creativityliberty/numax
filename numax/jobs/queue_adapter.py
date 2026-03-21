from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class QueueAdapter(ABC):
    @abstractmethod
    def enqueue(self, job_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def status(self, job_id: str) -> Dict[str, Any]:
        raise NotImplementedError
