import sys
import os

# Setup PATH
sys.path.append("/Volumes/Numtema/numax")

from numax.app import (
    startup_checks,
    profile_apply_cmd,
    recipe_run_cmd,
    mode_stats_cmd,
    mode_select_cmd,
    pack_install,
    sandbox_echo,
    spans_tail
)

print("=== 1. STARTUP CHECKS ===")
startup_checks()

print("\n=== 2. PROFILE APPLY (repo_operator) ===")
profile_apply_cmd(profile_id="repo_operator", preview=False)

print("\n=== 3. RECIPE RUN (workspace_audit) ===")
recipe_run_cmd(recipe_id="workspace_audit", preview=False)

print("\n=== 4. MODE STATS (by profile) ===")
# Note: mode_stats_cmd in app.py uses typer.echo, so it might not print if called directly
# unless we mock typer or use the internal function.
from numax.learning.mode_stats import compute_mode_stats
print(compute_mode_stats(group_by="profile"))

print("\n=== 5. SMART SELECTION ===")
from numax.learning.mode_selector import select_best_mode
print(select_best_mode(group_by="profile", min_runs=1))

print("\n=== 6. PACK INSTALL ===")
from numax.packs.install import install_pack
print(install_pack("numax_repo_bundle"))

print("\n=== 7. SANDBOX ECHO ===")
from numax.guardian.enforcer import enforce_sandbox_command
print(enforce_sandbox_command(user_roles=["admin"], command=["echo", "DEMO V2 SUCCESS"]))

print("\n=== 8. SPANS TAIL ===")
from pathlib import Path
path = Path("data/traces/spans.jsonl")
if path.exists():
    print(path.read_text().splitlines()[-5:])
else:
    print("No traces found yet.")
