from __future__ import annotations

from enum import IntEnum


class GovernancePriority(IntEnum):
    SAFETY = 100
    GOVERNANCE = 90
    USER_FIDELITY = 80
    QUALITY = 70
    CONTINUITY = 60
    COST = 50
    SPEED = 40
