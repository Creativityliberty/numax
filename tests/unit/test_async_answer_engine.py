import asyncio
from typing import Any

from numax.reason.async_answer import AsyncAnswerEngine


async def _run() -> dict[str, Any]:
    engine = AsyncAnswerEngine()
    return await engine.run("Explain NUMAX simply")


def test_async_answer_engine_runs() -> None:
    result = asyncio.run(_run())
    assert "candidate_output" in result
