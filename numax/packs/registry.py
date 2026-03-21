from __future__ import annotations

from typing import Dict

from numax.packs.signatures import sign_pack_payload
from numax.packs.specs import PackSpec


class PackRegistry:
    def __init__(self) -> None:
        self._packs: Dict[str, PackSpec] = {}

    def register(self, pack: PackSpec) -> None:
        self._packs[pack.pack_id] = pack

    def get(self, pack_id: str) -> PackSpec:
        return self._packs[pack_id]

    def list_ids(self) -> list[str]:
        return sorted(self._packs.keys())


def build_default_pack_registry() -> PackRegistry:
    registry = PackRegistry()
    pack = PackSpec(
        pack_id="numax_repo_bundle",
        title="NUMAX Repo Bundle",
        publisher="numax",
        trust_level="verified",
        profiles=["repo_operator"],
        recipes=["repo_repair_basic", "workspace_audit"],
        skills=["critic_strict"],
    )
    payload = f"{pack.pack_id}:{pack.publisher}:{pack.profiles}:{pack.recipes}:{pack.skills}"
    pack.signature = sign_pack_payload(payload)
    registry.register(pack)
    return registry
