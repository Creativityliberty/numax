from __future__ import annotations

import hashlib


def sign_pack_payload(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
