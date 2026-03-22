from __future__ import annotations

from abc import abstractmethod
from typing import Any, Dict, List

from numax.core.node import NumaxNode
from numax.core.state import NumaxState


class BatchNode(NumaxNode):
    name = "batch_node"

    @abstractmethod
    def exec_one(self, item: Any) -> Dict[str, Any]:
        raise NotImplementedError

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        items = payload.get("items", [])
        results: List[Dict[str, Any]] = []

        for item in items:
            results.append(self.exec_one(item))

        return {"batch_results": results}
