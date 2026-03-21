from __future__ import annotations

from numax.bootstrap import build_model_catalog, build_model_resolver
from numax.learning.model_selector import select_model_for_role
from numax.providers.async_bootstrap import build_async_provider_registry
from numax.providers.base import CompletionRequest
from numax.providers.errors import ProviderExecutionError


class AsyncAnswerEngine:
    def _build_prompt(self, user_input: str, retrieved_context: list[dict]) -> str:
        context_text = ""
        if retrieved_context:
            chunks = [
                f"[{item['source_id']}] {item['text']}"
                for item in retrieved_context
            ]
            context_text = "\n\nRetrieved context:\n" + "\n".join(chunks)
        return f"{user_input}{context_text}"

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

        for spec in catalog.list_by_role(role):
            row = spec.model_dump()
            if all(item["id"] != row["id"] for item in chain):
                chain.append(row)

        return chain

    async def run(
        self,
        user_input: str,
        retrieved_context: list[dict] | None = None,
        role: str = "primary",
    ) -> dict:
        retrieved_context = retrieved_context or []
        registry = build_async_provider_registry()
        prompt = self._build_prompt(user_input, retrieved_context)
        attempts: list[dict] = []

        for model_spec in self._candidate_chain(role):
            provider_name = model_spec["provider"]
            model_name = model_spec["model_name"]

            if provider_name not in registry.list_providers():
                attempts.append(
                    {
                        "provider": provider_name,
                        "model": model_name,
                        "ok": False,
                        "error": "provider_not_registered_async",
                    }
                )
                continue

            try:
                provider = registry.get(provider_name)
                health = await provider.ahealth()
                if not health.ok:
                    raise ProviderExecutionError(
                        f"Provider '{provider_name}' unhealthy: {health.notes}"
                    )

                response = await provider.acomplete(
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

        raise ProviderExecutionError(f"All async provider/model attempts failed: {attempts}")
