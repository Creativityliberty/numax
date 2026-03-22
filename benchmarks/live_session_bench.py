import sys
import time
from pathlib import Path

# Setup PATH
sys.path.append("/Volumes/Numtema/numax")

import numax
print(f"DEBUG: numax module path: {numax.__file__}")

from numax.learning.mode_feedback import capture_run_feedback, load_mode_feedback
from numax.learning.mode_selector import select_best_mode

def run_simulated_task(task_id: str, mode_id: str, success: bool, quality: float):
    print(f"--- Executing Task {task_id} with Mode {mode_id} ---")
    time.sleep(0.5)
    capture_run_feedback(
        run_id=f"live-{task_id}",
        target_id=mode_id,
        target_type="profile",
        ok=success,
        metrics={"quality_score": quality}
    )
    print(f"Feedback recorded: success={success}, quality={quality}")

def main():
    print("=== LIVE LEARNING SESSION START ===")
    
    # 1. Initial State
    print("\n[Step 1] Initial Recommendation (Zero knowledge or mock base):")
    print(select_best_mode(group_by="profile"))
    
    # 2. Injecting failure for 'research_mode'
    print("\n[Step 2] Simulated failures for 'research_mode' (bad quality/success)...")
    for i in range(3):
        run_simulated_task(f"R{i}", "research_mode", success=False, quality=0.2)
        
    # 3. Injecting success for 'repo_operator'
    print("\n[Step 3] Simulated success for 'repo_operator' (high quality)...")
    for i in range(3):
        run_simulated_task(f"S{i}", "repo_operator", success=True, quality=0.9)
        
    # 4. Final State check
    print("\n[Step 4] New Recommendation after learning:")
    result = select_best_mode(group_by="profile", min_runs=1)
    print(f"Selected: {result['selected']} with score {result['score']:.2f}")
    
    print("\n=== LIVE LEARNING SESSION COMPLETE ===")

if __name__ == "__main__":
    main()
