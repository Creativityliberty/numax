from __future__ import annotations

from typing import Any, Dict

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.teams.artifact_bus import publish_artifact
from numax.teams.blackboard import BlackboardState, list_blackboard_entries
from numax.teams.message_queue import TeamMessageQueue, dequeue_messages_for_team


class BlackboardPublishNode(NumaxNode):
    name = "blackboard_publish"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "team_id": state.observation.get("team_id", "product_squad"),
            "artifact_type": state.observation.get("artifact_type", "spec"),
            "payload": state.observation.get("artifact_payload", {}),
            "blackboard_state": state.blackboard_state,
            "mission_queue": state.mission_queue,
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        blackboard = BlackboardState(**payload["blackboard_state"])
        queue = TeamMessageQueue(**payload["mission_queue"])

        result = publish_artifact(
            blackboard=blackboard,
            queue=queue,
            team_id=payload["team_id"],
            artifact_type=payload["artifact_type"],
            payload=payload["payload"],
        )

        return {
            "publish_result": result,
            "blackboard_state": blackboard.model_dump(),
            "mission_queue": queue.model_dump(),
        }

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        state.blackboard_state = result["blackboard_state"]
        state.mission_queue = result["mission_queue"]
        state.next_recommended_action = "consume_blackboard_updates"
        state.add_trace(
            self.name,
            "post",
            "Artifact published to blackboard",
            artifact_type=payload["artifact_type"],
            subscribers=result["publish_result"]["subscribers"],
        )
        return "consume"


class BlackboardConsumeNode(NumaxNode):
    name = "blackboard_consume"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "team_id": state.observation.get("consume_team_id", "engineering_squad"),
            "mission_queue": state.mission_queue,
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        queue = TeamMessageQueue(**payload["mission_queue"])
        queue, taken = dequeue_messages_for_team(queue, payload["team_id"])
        return {
            "messages": taken,
            "mission_queue": queue.model_dump(),
        }

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        state.mission_queue = result["mission_queue"]
        state.subscription_state[payload["team_id"]] = result["messages"]
        state.next_recommended_action = "trigger_team_flow" if result["messages"] else "idle_wait"
        state.add_trace(
            self.name,
            "post",
            "Team consumed messages from queue",
            team_id=payload["team_id"],
            message_count=len(result["messages"]),
        )
        return "done"
