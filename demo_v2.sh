#!/bin/bash
# NUMAX V2 Demo Script

export PYTHONPATH=$PYTHONPATH:.
PYTHON_BIN="/Volumes/Numtema/numax/venv/bin/python3.14"

echo "--- 1. STARTUP CHECKS ---"
$PYTHON_BIN numax/app.py startup-checks

echo -e "\n--- 2. PROFILE APPLICATION (Learning Entry 1) ---"
$PYTHON_BIN numax/app.py profile-apply --profile-id repo_operator --no-preview

echo -e "\n--- 3. RECIPE EXECUTION (Learning Entry 2) ---"
$PYTHON_BIN numax/app.py recipe-run --recipe-id workspace_audit --no-preview

echo -e "\n--- 4. MODE FEEDBACK SHOW ---"
$PYTHON_BIN numax/app.py mode-feedback-show

echo -e "\n--- 5. SMART MODE SELECTION ---"
$PYTHON_BIN numax/app.py mode-select --group-by profile --min-runs 1

echo -e "\n--- 6. PACKS & TRUST ---"
$PYTHON_BIN numax/app.py pack-install --pack-id numax_repo_bundle

echo -e "\n--- 7. SANDBOX ENFORCEMENT ---"
echo "Trying 'echo hello' (Allowed):"
$PYTHON_BIN numax/app.py sandbox-echo --message "Hello NUMAX V2"

echo -e "\n--- 8. OBSERVABILITY (Tail Spans) ---"
$PYTHON_BIN numax/app.py spans-tail
