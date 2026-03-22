from __future__ import annotations

from typing import Any, Dict


def skill_to_profile(item: Dict[str, Any]) -> Dict[str, Any] | None:
    skill_id = item["skill_id"]

    mapping = {
        "nanoclaw-forge": {
            "profile_id": "meta_factory",
            "title": "Meta Factory",
            "description": "Global PLAN → MAP → BUILD → RUN → SHIP posture.",
            "skills": ["critic_strict"],
        },
        "kernel-forge": {
            "profile_id": "kernel_builder",
            "title": "Kernel Builder",
            "description": "Policy-gated kernel-oriented runtime posture.",
            "skills": [],
        },
        "flow-orchestrator": {
            "profile_id": "flow_runtime",
            "title": "Flow Runtime",
            "description": "Tracing, snapshots, pause/resume oriented runtime posture.",
            "skills": [],
        },
        "num-agents": {
            "profile_id": "agent_sdk_mode",
            "title": "Agent SDK Mode",
            "description": "Agent-oriented runtime posture.",
            "skills": [],
        },
    }

    return mapping.get(skill_id)
