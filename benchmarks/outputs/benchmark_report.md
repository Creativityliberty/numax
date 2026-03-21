# NUMAX Benchmark Report

## llm_only
- **task_success_rate**: 1.0
- **artifact_validity_rate**: 0.0
- **recovery_success_rate**: 0.3333333333333333
- **continuity_resume_score**: 0.26666666666666666
- **budget_efficiency_score**: 0.9345794392523364
- **mutation_safety_score**: 0.0
- **count**: 6

## llm_tools
- **task_success_rate**: 1.0
- **artifact_validity_rate**: 0.0
- **recovery_success_rate**: 0.3333333333333333
- **continuity_resume_score**: 0.31666666666666665
- **budget_efficiency_score**: 0.9132420091324202
- **mutation_safety_score**: 0.0
- **count**: 6

## llm_tools_memory
- **task_success_rate**: 1.0
- **artifact_validity_rate**: 0.0
- **recovery_success_rate**: 0.3333333333333333
- **continuity_resume_score**: 0.4083333333333334
- **budget_efficiency_score**: 0.903342366757001
- **mutation_safety_score**: 0.0
- **count**: 6

## numax
- **task_success_rate**: 1.0
- **artifact_validity_rate**: 0.16666666666666666
- **recovery_success_rate**: 1.0
- **continuity_resume_score**: 0.4000000000000001
- **budget_efficiency_score**: 1.0
- **mutation_safety_score**: 0.0
- **count**: 6

## Scenario Results

- `numax` on `long_task` => success=True artifact_valid=True recovered=True tokens=0 cost=0.0
- `llm_only` on `long_task` => success=True artifact_valid=False recovered=True tokens=500 cost=0.02
- `llm_tools` on `long_task` => success=True artifact_valid=False recovered=True tokens=650 cost=0.03
- `llm_tools_memory` on `long_task` => success=True artifact_valid=False recovered=True tokens=720 cost=0.035
- `numax` on `retrieval_failure` => success=True artifact_valid=False recovered=True tokens=0 cost=0.0
- `llm_only` on `retrieval_failure` => success=True artifact_valid=False recovered=False tokens=500 cost=0.02
- `llm_tools` on `retrieval_failure` => success=True artifact_valid=False recovered=False tokens=650 cost=0.03
- `llm_tools_memory` on `retrieval_failure` => success=True artifact_valid=False recovered=False tokens=720 cost=0.035
- `numax` on `provider_failure` => success=True artifact_valid=False recovered=True tokens=0 cost=0.0
- `llm_only` on `provider_failure` => success=True artifact_valid=False recovered=False tokens=500 cost=0.02
- `llm_tools` on `provider_failure` => success=True artifact_valid=False recovered=False tokens=650 cost=0.03
- `llm_tools_memory` on `provider_failure` => success=True artifact_valid=False recovered=False tokens=720 cost=0.035
- `numax` on `budget_overflow` => success=True artifact_valid=False recovered=True tokens=0 cost=0.0
- `llm_only` on `budget_overflow` => success=True artifact_valid=False recovered=False tokens=500 cost=0.02
- `llm_tools` on `budget_overflow` => success=True artifact_valid=False recovered=False tokens=650 cost=0.03
- `llm_tools_memory` on `budget_overflow` => success=True artifact_valid=False recovered=False tokens=720 cost=0.035
- `numax` on `continuity_resume` => success=True artifact_valid=False recovered=True tokens=0 cost=0.0
- `llm_only` on `continuity_resume` => success=True artifact_valid=False recovered=True tokens=500 cost=0.02
- `llm_tools` on `continuity_resume` => success=True artifact_valid=False recovered=True tokens=650 cost=0.03
- `llm_tools_memory` on `continuity_resume` => success=True artifact_valid=False recovered=True tokens=720 cost=0.035
- `numax` on `mutation_rollback` => success=True artifact_valid=False recovered=True tokens=0 cost=0.0
- `llm_only` on `mutation_rollback` => success=True artifact_valid=False recovered=False tokens=500 cost=0.02
- `llm_tools` on `mutation_rollback` => success=True artifact_valid=False recovered=False tokens=650 cost=0.03
- `llm_tools_memory` on `mutation_rollback` => success=True artifact_valid=False recovered=False tokens=720 cost=0.035