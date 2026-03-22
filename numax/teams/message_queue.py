from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class TeamMessage(BaseModel):
    from_team: str
    to_team: str
    topic: str
    payload: Dict[str, Any] = Field(default_factory=dict)


class TeamMessageQueue(BaseModel):
    messages: List[TeamMessage] = Field(default_factory=list)


def enqueue_message(queue: TeamMessageQueue, message: TeamMessage) -> TeamMessageQueue:
    queue.messages.append(message)
    return queue


def dequeue_messages_for_team(queue: TeamMessageQueue, team_id: str) -> tuple[TeamMessageQueue, list[dict]]:
    taken: list[dict] = []
    remaining: list[TeamMessage] = []

    for message in queue.messages:
        if message.to_team == team_id:
            taken.append(message.model_dump())
        else:
            remaining.append(message)

    queue.messages = remaining
    return queue, taken
