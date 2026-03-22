from __future__ import annotations

import uuid
from typing import Any, Dict

from numax.teams.blackboard import BlackboardEntry, BlackboardState, add_blackboard_entry
from numax.teams.message_queue import TeamMessage, TeamMessageQueue, enqueue_message
from numax.teams.subscriptions import get_subscribers


def publish_artifact(
    blackboard: BlackboardState,
    queue: TeamMessageQueue,
    team_id: str,
    artifact_type: str,
    payload: Dict[str, Any],
) -> dict:
    entry = BlackboardEntry(
        entry_id=str(uuid.uuid4()),
        team_id=team_id,
        artifact_type=artifact_type,
        payload=payload,
        tags=[artifact_type, team_id],
    )
    add_blackboard_entry(blackboard, entry)

    subscribers = get_subscribers(artifact_type)
    for target_team in subscribers:
        enqueue_message(
            queue,
            TeamMessage(
                from_team=team_id,
                to_team=target_team,
                topic=f"{artifact_type}_published",
                payload=payload,
            ),
        )

    return {
        "entry": entry.model_dump(),
        "subscribers": subscribers,
    }
