from __future__ import annotations

import json
import uuid
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP

from numax.core.state import NumaxState
from numax.flows.planning_execution import build_planning_execution_flow

mcp = FastMCP("NumaxMCP")


@mcp.tool()
def execute_numax_plan(prompt: str) -> str:
    """
    Exécute un plan complet NUMAX (Intent -> Plan -> Retrieve -> Answer -> Critique) basé sur un prompt.
    Renvoie le résultat complet avec la critique et l'identité de l'exécution.
    """
    state = NumaxState(
        observation={"raw_input": prompt},
    )
    state.runtime.run_id = str(uuid.uuid4())
    state.world_state["autonomy_mode"] = "ASSISTED"

    graph = build_planning_execution_flow()
    final_state = graph.run(start="intent_router", state=state)

    output = {
        "run_id": final_state.runtime.run_id,
        "final_output": final_state.final_output,
        "plan": final_state.plan,
        "critique": final_state.critique.model_dump() if final_state.critique else None,
        "trace_summary": [
            f"[{e.node}::{e.phase}] {e.message}" for e in final_state.trace
        ],
    }

    return json.dumps(output, indent=2)


if __name__ == "__main__":
    mcp.run_stdio_async()
