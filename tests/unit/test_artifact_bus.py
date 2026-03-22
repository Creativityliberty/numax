from numax.teams.artifact_bus import publish_artifact
from numax.teams.blackboard import BlackboardState
from numax.teams.message_queue import TeamMessageQueue


def test_publish_artifact_notifies_subscribers():
    blackboard = BlackboardState()
    queue = TeamMessageQueue()

    result = publish_artifact(
        blackboard=blackboard,
        queue=queue,
        team_id="product_squad",
        artifact_type="spec",
        payload={"objective": "Ship feature"},
    )

    assert result["subscribers"] == ["engineering_squad"]
    assert len(blackboard.entries) == 1
    assert len(queue.messages) == 1
