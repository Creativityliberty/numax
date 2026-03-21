Oui chef.
Voilà le starter kit réel pour NUMAX v0.1 avec les 4 fichiers de base :

state.py
node.py
graph.py
intent.py

Je te les écris pour qu’ils soient :

simples,
typés,
testables,
cohérents entre eux,
assez propres pour servir de socle.
1. numax/core/state.py
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


FsmState = Literal[
    "IDLE",
    "UNDERSTAND",
    "PLAN",
    "BUILD",
    "DELIVER",
    "LEARN",
    "DEGRADED",
    "HALT",
]


class RuntimeState(BaseModel):
    fsm_state: FsmState = "IDLE"
    flow_name: Optional[str] = None
    owner: Optional[str] = None
    run_id: Optional[str] = None
    retries: int = 0
    degraded: bool = False


class BudgetState(BaseModel):
    max_tokens_total: Optional[int] = None
    max_cost_usd: Optional[float] = None
    tokens_used: int = 0
    cost_used_usd: float = 0.0


class ConfidenceState(BaseModel):
    understanding_confidence: float = 0.0
    source_confidence: float = 0.0
    output_confidence: float = 0.0
    safety_confidence: float = 1.0


class CritiqueState(BaseModel):
    ok: bool = True
    notes: List[str] = Field(default_factory=list)
    confidence: float = 0.0


class TraceEvent(BaseModel):
    node: str
    phase: Literal["prep", "exec", "post", "fallback", "transition", "error"]
    message: str
    data: Dict[str, Any] = Field(default_factory=dict)


class NumaxState(BaseModel):
    goal: Dict[str, Any] = Field(default_factory=dict)
    observation: Dict[str, Any] = Field(default_factory=dict)
    world_state: Dict[str, Any] = Field(default_factory=dict)
    memory: Dict[str, Any] = Field(
        default_factory=lambda: {
            "working": {},
            "continuity": {},
        }
    )
    retrieved_context: List[Dict[str, Any]] = Field(default_factory=list)
    plan: Optional[Dict[str, Any]] = None
    candidate_output: Optional[Any] = None
    critique: Optional[CritiqueState] = None
    final_output: Optional[Any] = None
    runtime: RuntimeState = Field(default_factory=RuntimeState)
    budget: BudgetState = Field(default_factory=BudgetState)
    confidence: ConfidenceState = Field(default_factory=ConfidenceState)
    trace: List[TraceEvent] = Field(default_factory=list)

    def add_trace(
        self,
        node: str,
        phase: Literal["prep", "exec", "post", "fallback", "transition", "error"],
        message: str,
        **data: Any,
    ) -> None:
        self.trace.append(
            TraceEvent(
                node=node,
                phase=phase,
                message=message,
                data=data,
            )
        )
2. numax/core/node.py
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
3. numax/core/graph.py
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
4. numax/router/intent.py
from __future__ import annotations

from typing import Any, Dict

from numax.core.node import NumaxNode
from numax.core.state import NumaxState


class IntentRouterNode(NumaxNode):
    name = "intent_router"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        state.runtime.fsm_state = "UNDERSTAND"

        user_input = state.observation.get("raw_input", "")
        retrieved_context = state.retrieved_context
        source_conf = state.confidence.source_confidence

        payload = {
            "user_input": user_input,
            "has_context": len(retrieved_context) > 0,
            "source_confidence": source_conf,
        }
        state.add_trace(self.name, "prep", "Intent router payload prepared", **payload)
        return payload

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        text = str(payload["user_input"]).strip().lower()

        needs_retrieval_keywords = [
            "source",
            "document",
            "file",
            "reference",
            "citation",
            "research",
            "search",
            "look up",
        ]

        if any(keyword in text for keyword in needs_retrieval_keywords):
            return {
                "route": "retrieve",
                "understanding_confidence": 0.85,
            }

        if payload["has_context"] and payload["source_confidence"] >= 0.5:
            return {
                "route": "answer",
                "understanding_confidence": 0.80,
            }

        return {
            "route": "answer",
            "understanding_confidence": 0.70,
        }

    def post(
        self,
        state: NumaxState,
        payload: Dict[str, Any],
        result: Dict[str, Any],
    ) -> str:
        route = result["route"]
        state.confidence.understanding_confidence = result["understanding_confidence"]
        state.world_state["intent_route"] = route

        if route == "retrieve":
            state.runtime.fsm_state = "PLAN"
            return "retrieve"

        state.runtime.fsm_state = "BUILD"
        return "answer"
5. Bonus utile : numax/reason/answer.py

Comme ça, tu as tout de suite un flow qui tourne.

from __future__ import annotations

from typing import Any, Dict

from numax.core.node import NumaxNode
from numax.core.state import CritiqueState, NumaxState


class AnswerNode(NumaxNode):
    name = "answer"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        payload = {
            "user_input": state.observation.get("raw_input", ""),
            "retrieved_context": state.retrieved_context,
        }
        state.add_trace(self.name, "prep", "Answer payload prepared")
        return payload

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        user_input = payload["user_input"]
        retrieved_context = payload["retrieved_context"]

        if retrieved_context:
            answer = {
                "text": f"Réponse basée sur le contexte récupéré pour : {user_input}",
                "used_context": True,
            }
        else:
            answer = {
                "text": f"Réponse simple à : {user_input}",
                "used_context": False,
            }

        return {"candidate_output": answer}

    def post(
        self,
        state: NumaxState,
        payload: Dict[str, Any],
        result: Dict[str, Any],
    ) -> str:
        state.candidate_output = result["candidate_output"]
        state.confidence.output_confidence = 0.75
        state.runtime.fsm_state = "DELIVER"
        return "critic"
6. Bonus utile : numax/critic/basic.py
from __future__ import annotations

from typing import Any, Dict

from numax.core.node import NumaxNode
from numax.core.state import CritiqueState, NumaxState


class BasicCriticNode(NumaxNode):
    name = "basic_critic"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        payload = {
            "candidate_output": state.candidate_output,
            "safety_confidence": state.confidence.safety_confidence,
        }
        state.add_trace(self.name, "prep", "Critic payload prepared")
        return payload

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        notes = []
        ok = True

        if payload["candidate_output"] is None:
            ok = False
            notes.append("No candidate output produced.")

        if payload["safety_confidence"] < 0.6:
            ok = False
            notes.append("Safety confidence too low.")

        return {
            "ok": ok,
            "notes": notes,
            "confidence": 0.80 if ok else 0.30,
        }

    def post(
        self,
        state: NumaxState,
        payload: Dict[str, Any],
        result: Dict[str, Any],
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
7. Bonus utile : numax/flows/basic_chat.py
from numax.core.graph import NumaxGraph
from numax.router.intent import IntentRouterNode
from numax.reason.answer import AnswerNode
from numax.critic.basic import BasicCriticNode


def build_basic_chat_flow() -> NumaxGraph:
    graph = NumaxGraph(name="basic_chat")

    router = IntentRouterNode()
    answer = AnswerNode()
    critic = BasicCriticNode()

    graph.add_node(router)
    graph.add_node(answer)
    graph.add_node(critic)

    graph.add_edge("intent_router", "answer", "answer")
    graph.add_edge("intent_router", "retrieve", "answer")  # stub v0.1
    graph.add_edge("answer", "critic", "basic_critic")
    graph.add_edge("basic_critic", "done", None)
    graph.add_edge("basic_critic", "halt", None)

    return graph
8. Bonus utile : numax/app.py
from __future__ import annotations

import uuid

import typer

from numax.core.state import NumaxState
from numax.flows.basic_chat import build_basic_chat_flow

app = typer.Typer()


@app.command()
def run(
    flow: str = typer.Option("basic_chat", help="Flow name"),
    prompt: str = typer.Option(..., help="User input"),
) -> None:
    if flow != "basic_chat":
        raise typer.BadParameter(f"Unsupported flow for now: {flow}")

    state = NumaxState(
        observation={"raw_input": prompt},
    )
    state.runtime.run_id = str(uuid.uuid4())

    graph = build_basic_chat_flow()
    final_state = graph.run(start="intent_router", state=state)

    typer.echo("=== FINAL OUTPUT ===")
    typer.echo(final_state.final_output)

    typer.echo("\n=== TRACE ===")
    for event in final_state.trace:
        typer.echo(f"[{event.node}::{event.phase}] {event.message}")


if __name__ == "__main__":
    app()
9. Commande pour tester
python -m numax.app run --prompt "Explique NUMAX simplement"
10. Ce que ça t’apporte tout de suite

Avec juste ces fichiers, tu as déjà :

un état typé
un contrat de nœud
un graphe exécutable
un routeur d’intention
un nœud de réponse
un critic minimal
une trace
un FSM de base
une CLI de test

Donc ce n’est plus du pur concept.
C’est déjà un noyau exécutable.

11. Ordre des prochains fichiers à écrire

Ensuite, dans cet ordre :

numax/retrieve/engine.py
numax/providers/base.py
numax/providers/registry.py
numax/models/catalog.py
numax/models/resolver.py
numax/runtime/budget.py
numax/critic/confidence.py
numax/memory/continuity.py

La meilleure suite maintenant, c’est que je te fasse le pack suivant directement codé :

providers/base.py
providers/registry.py
models/catalog.py
models/resolver.py