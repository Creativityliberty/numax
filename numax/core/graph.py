from __future__ import annotations

from typing import Dict, Optional, Tuple

from numax.core.node import NumaxNode
from numax.core.state import NumaxState


class NumaxGraph:
    def __init__(self, name: str):
        self.name = name
        self.nodes: Dict[str, NumaxNode] = {}
        self.edges: Dict[Tuple[str, str], Optional[str]] = {}

    def add_node(self, node: NumaxNode) -> None:
        if node.name in self.nodes:
            raise ValueError(f"Node '{node.name}' already exists in graph '{self.name}'.")
        self.nodes[node.name] = node

    def add_edge(self, source: str, transition: str, target: Optional[str]) -> None:
        if source not in self.nodes:
            raise ValueError(f"Unknown source node: {source}")
        if target is not None and target not in self.nodes:
            raise ValueError(f"Unknown target node: {target}")
        self.edges[(source, transition)] = target

    def run(self, start: str, state: NumaxState) -> NumaxState:
        if start not in self.nodes:
            raise ValueError(f"Unknown start node: {start}")

        state.runtime.flow_name = self.name
        current = start

        while current is not None:
            node = self.nodes[current]
            transition = node.run(state)
            current = self.edges.get((node.name, transition))

        return state
