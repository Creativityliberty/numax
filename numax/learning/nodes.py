from __future__ import annotations

from typing import Any, Dict

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.learning.mode_feedback import capture_run_feedback
from numax.learning.mode_selector import SmartModeSelector
from numax.learning.mode_stats import ModeFeedback, build_mock_history


class LearningFeedbackNode(NumaxNode):
    name = "learning_feedback"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        target_id = state.active_recipe or state.active_profile or "unknown"
        target_type = "recipe" if state.active_recipe else "profile"
        
        return {
            "run_id": state.runtime.run_id,
            "target_id": target_id,
            "target_type": target_type,
            "ok": state.next_recommended_action != "inspect_failure", # Simplified
            "metrics": {
                "outcome_summary": state.next_recommended_action,
                "context_tags": state.world_state.get("tags", []),
            }
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        feedback = capture_run_feedback(
            run_id=payload["run_id"],
            target_id=payload["target_id"],
            target_type=payload["target_type"],
            ok=payload["ok"],
            metrics=payload["metrics"],
        )
        return {"feedback": feedback.model_dump()}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        feedback_data = result["feedback"]
        state.active_feedback = feedback_data
        state.learning_history.append(feedback_data)
        
        state.add_trace(
            self.name,
            "post",
            "Learning feedback captured",
            target_id=payload["target_id"],
            ok=payload["ok"],
        )
        return "done"


class LearningRecommendNode(NumaxNode):
    name = "learning_recommend"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "task_type": state.observation.get("task_type", "general"),
            "candidates": state.observation.get("mode_candidates", ["repo_operator", "research_mode"]),
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # In a real scenario, we would load the external history. Here we use mock + state history.
        history_objs = [ModeFeedback(**h) for h in []] # Placeholder for persistent storage
        selector = SmartModeSelector(history=history_objs + build_mock_history())
        
        recommendation = selector.recommend(
            task_type=payload["task_type"],
            candidates=payload["candidates"],
        )
        return {"recommendation": recommendation}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        recommendation = result["recommendation"]
        state.mode_recommendation = recommendation
        state.next_recommended_action = f"apply_{recommendation['recommended_id']}"
        
        state.add_trace(
            self.name,
            "post",
            "Mode recommendation generated",
            recommended_id=recommendation["recommended_id"],
        )
        return "done"
