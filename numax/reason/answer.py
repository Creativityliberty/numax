from __future__ import annotations

from typing import Any

from numax.bootstrap import build_model_catalog, build_model_resolver, build_provider_registry
from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.learning.model_selector import select_model_for_role
from numax.providers.base import CompletionRequest
from numax.providers.errors import ProviderExecutionError
from numax.runtime.budget import BudgetCharge, charge_budget


class AnswerNode(NumaxNode):
    name = "answer"

    def prep(self, state: NumaxState) -> dict[str, Any]:
        payload = {
            "user_input": state.observation.get("raw_input", ""),
            "retrieved_context": state.retrieved_context,
        }
        state.add_trace(self.name, "prep", "Answer payload prepared")
        return payload

    def _build_prompt(self, payload: dict[str, Any]) -> str:
        context_text = ""
        if payload["retrieved_context"]:
            chunks = [
                f"[{item['source_id']}] {item['text']}" for item in payload["retrieved_context"]
            ]
            context_text = "\n\nRetrieved context:\n" + "\n".join(chunks)
        return f"{payload['user_input']}{context_text}"

    def _candidate_chain(self, role: str = "primary") -> list[dict]:
        chosen = select_model_for_role(role)
        catalog = build_model_catalog()
        resolver = build_model_resolver(catalog)

        chain: list[dict] = [chosen]
        try:
            preferred = resolver.policy.preferred.get(role)
            if preferred and preferred != chosen["id"]:
                spec = catalog.get(preferred)
                chain.append(spec.model_dump())
        except Exception:
            pass

        for fallback_id in resolver.policy.fallbacks.get(role, []):
            if all(item["id"] != fallback_id for item in chain):
                try:
                    spec = catalog.get(fallback_id)
                    chain.append(spec.model_dump())
                except Exception:
                    continue

        role_candidates = catalog.list_by_role(role)
        for spec in role_candidates:
            row = spec.model_dump()
            if all(item["id"] != row["id"] for item in chain):
                chain.append(row)

        return chain

    def exec(self, payload: dict[str, Any]) -> dict[str, Any]:
        registry = build_provider_registry()
        prompt = self._build_prompt(payload)
        attempts: list[dict] = []

        for model_spec in self._candidate_chain("primary"):
            provider_name = model_spec["provider"]
            model_name = model_spec["model_name"]
            try:
                provider = registry.get(provider_name)
                health = provider.health()
                if not health.ok:
                    raise ProviderExecutionError(
                        f"Provider '{provider_name}' unhealthy: {health.notes}"
                    )

                response = provider.complete(
                    model=model_name,
                    request=CompletionRequest(prompt=prompt, response_format="text"),
                )

                return {
                    "candidate_output": {
                        "text": response.content,
                        "provider": response.provider,
                        "model": response.model,
                        "usage": response.usage,
                    },
                    "provider_attempts": attempts
                    + [
                        {
                            "provider": provider_name,
                            "model": model_name,
                            "ok": True,
                        }
                    ],
                }
            except Exception as exc:
                attempts.append(
                    {
                        "provider": provider_name,
                        "model": model_name,
                        "ok": False,
                        "error": str(exc),
                    }
                )
                continue

        raise ProviderExecutionError(f"All provider/model attempts failed: {attempts}")

    def post(
        self,
        state: NumaxState,
        payload: dict[str, Any],
        result: dict[str, Any],
    ) -> str:
        state.candidate_output = result["candidate_output"]
        state.world_state["provider_attempts"] = result.get("provider_attempts", [])
        state.confidence.output_confidence = 0.75

        tool_history = state.memory.setdefault("tool_history", [])
        for attempt in result.get("provider_attempts", []):
            tool_history.append(
                {
                    "tool": f"provider.{attempt['provider']}",
                    "model": attempt["model"],
                    "ok": attempt["ok"],
                    "error": attempt.get("error"),
                }
            )

        usage = result["candidate_output"].get("usage", {})
        charge_budget(
            state,
            BudgetCharge(
                tokens=int(usage.get("input_tokens", 0)) + int(usage.get("output_tokens", 0)),
                cost_usd=0.0,
            ),
        )

        state.runtime.fsm_state = "DELIVER"
        return "critic"
