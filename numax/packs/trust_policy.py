from __future__ import annotations

from numax.packs.specs import PackSpec


def evaluate_pack_trust(pack: PackSpec) -> dict:
    if pack.trust_level == "verified" and pack.signature:
        return {"ok": True, "decision": "allow", "reason": "verified_pack"}
    if pack.trust_level == "trusted":
        return {"ok": True, "decision": "allow_with_review", "reason": "trusted_pack"}
    return {"ok": False, "decision": "deny", "reason": "untrusted_pack"}
