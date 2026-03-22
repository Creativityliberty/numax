from __future__ import annotations

from fastapi import APIRouter
from numax.learning.mode_stats import compute_mode_stats
from numax.learning.mode_selector import select_best_mode, SmartModeSelector
from numax.learning.mode_feedback import load_mode_feedback
from numax.learning.mode_stats import ModeFeedback, build_mock_history
from numax.server.schemas import (
    LearningStatsResponse,
    ModeRecommendationRequest,
    ModeRecommendationResponse,
)

router = APIRouter()


@router.get("/stats", response_model=LearningStatsResponse)
def get_learning_stats(group_by: str = "profile") -> dict:
    return compute_mode_stats(group_by=group_by)


@router.post("/recommend", response_model=ModeRecommendationResponse)
def get_mode_recommendation(request: ModeRecommendationRequest) -> dict:
    # Use real history + mock for demo
    feedback_payload = load_mode_feedback()
    history_objs = [ModeFeedback(**r) for r in feedback_payload.get("records", [])]
    
    selector = SmartModeSelector(history=history_objs + build_mock_history())
    recommendation = selector.recommend(
        task_type=request.task_type,
        candidates=request.candidates,
    )
    return recommendation


@router.get("/best")
def get_best_mode(group_by: str = "profile") -> dict:
    return select_best_mode(group_by=group_by, min_runs=1)
