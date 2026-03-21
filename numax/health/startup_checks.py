from __future__ import annotations

from dataclasses import dataclass, field

from numax.identity.runtime_identity import build_runtime_identity


@dataclass
class StartupCheckResult:
    ok: bool
    notes: list[str] = field(default_factory=list)


def run_startup_checks(autonomy_mode: str = "ASSISTED") -> StartupCheckResult:
    identity = build_runtime_identity(autonomy_mode=autonomy_mode)
    notes: list[str] = []
    ok = True

    if not identity["version"]:
        ok = False
        notes.append("Missing runtime version.")

    if not identity["providers"]:
        ok = False
        notes.append("No providers registered.")

    if not identity["models"]:
        ok = False
        notes.append("No models available in catalog.")

    if autonomy_mode not in {
        "ASSISTED",
        "SEMI_AUTONOMOUS",
        "BOUNDED_AUTONOMOUS",
        "SUPERVISED_AUTONOMOUS",
    }:
        ok = False
        notes.append(f"Unknown autonomy mode: {autonomy_mode}")

    if ok:
        notes.append("Startup checks passed.")

    return StartupCheckResult(ok=ok, notes=notes)
