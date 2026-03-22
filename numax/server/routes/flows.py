from __future__ import annotations

import uuid
from fastapi import APIRouter, HTTPException
from numax.core.state import NumaxState
from numax.server.schemas import RunRequest, RunResponse

# This is a simplified dynamic importer for flows
def get_flow_builder(name: str):
    try:
        if name == "basic_chat":
            from numax.flows.basic_chat import build_basic_chat_flow
            return build_basic_chat_flow, "intent_router"
        elif name == "workspace_analysis":
            from numax.flows.workspace_analysis import build_workspace_analysis_flow
            return build_workspace_analysis_flow, "workspace_open"
        elif name == "repo_repair":
            from numax.flows.repo_repair import build_repo_repair_flow
            return build_repo_repair_flow, "workspace_open"
        elif name == "learning_feedback":
            from numax.flows.learning_feedback import build_learning_feedback_flow
            return build_learning_feedback_flow, "learning_feedback"
        # Add more mappings as needed
        raise ValueError(f"Unknown flow: {name}")
    except ImportError as e:
        raise HTTPException(status_code=500, detail=f"Flow engine import failed: {str(e)}")


router = APIRouter()


@router.post("/run", response_model=RunResponse)
def run_flow(request: RunRequest) -> dict:
    builder, start_node = get_flow_builder(request.flow)
    
    state = NumaxState(
        observation={
            "raw_input": request.prompt,
            "workspace_path": request.workspace_path or ".",
            **request.overrides
        }
    )
    state.runtime.run_id = str(uuid.uuid4())
    
    graph = builder()
    final_state = graph.run(start=start_node, state=state)
    
    return {
        "run_id": final_state.runtime.run_id,
        "flow": request.flow,
        "output": final_state.final_output or final_state.world_state,
        "next_action": final_state.next_recommended_action,
    }
