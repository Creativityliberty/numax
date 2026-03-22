from numax.teams.message_queue import TeamMessage, TeamMessageQueue, enqueue_message, dequeue_messages_for_team


def test_message_queue_roundtrip():
    queue = TeamMessageQueue()
    enqueue_message(
        queue,
        TeamMessage(
            from_team="product_squad",
            to_team="engineering_squad",
            topic="spec_published",
            payload={"objective": "Build X"},
        ),
    )

    queue, messages = dequeue_messages_for_team(queue, "engineering_squad")
    assert len(messages) == 1
    assert queue.messages == []
