from __future__ import annotations

from dataclasses import dataclass

from numax.packs.registry import build_default_pack_registry
from numax.packs.trust_policy import evaluate_pack_trust


@dataclass
class PackInstallResult:
    ok: bool
    pack_id: str
    notes: list[str]


def install_pack(pack_id: str) -> PackInstallResult:
    registry = build_default_pack_registry()
    pack = registry.get(pack_id)
    trust = evaluate_pack_trust(pack)

    notes: list[str] = [f"Pack '{pack_id}' evaluated.", f"Trust decision: {trust}"]
    if not trust["ok"]:
        return PackInstallResult(ok=False, pack_id=pack_id, notes=notes)

    notes.append("Pack install allowed. Apply contained profiles/recipes/skills through dedicated loaders.")
    return PackInstallResult(ok=True, pack_id=pack_id, notes=notes)
