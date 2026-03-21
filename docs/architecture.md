# NUMAX Architecture

This document serves as the high-level map of the NUMAX Agentic Cortex. If you are reading this codebase for the first time, this is your entry point.

## Core Philosophy
NUMAX treats agentic behavior not as a magical black-box LLM call, but as a deterministic mathematical graph. The architecture is explicitly split into distinct, governed layers to control cost, ensure safety, and output verifiable artifacts.

## Directory Map

### 1. The Core Infrastructure
- `numax/core/`: The absolute foundation. Contains `NumaxState` (typed Pydantic state), `NumaxNode` (contract for all nodes), and `NumaxGraph` (the FSM runtime executing the nodes).
- `numax/runtime/`: The execution supervisor. Tracks budgets, limits, and stop conditions.
- `numax/errors/`: Taxonomies of failures (Understanding, Safety, Protocol) and matching resilient policies (Retry, Degrade, Halt).

### 2. The Cognitive Layers
These layers map directly to the states inside the NUMAX FSM master plan.
- `numax/router/`: Intent clarification and flow branching (`IntentRouterNode`).
- `numax/retrieve/`: Context gathering and memory indexing.
- `numax/planner/`: Objective decomposition (`TaskMorsel` creation).
- `numax/reason/`: Generation, synthesis, and answer building.
- `numax/critic/`: Internal evaluation. Modulates confidence levels to dictate the next FSM transition.

### 3. The Physical/External World
- `numax/tools/`: Tool registry and execution.
- `numax/sandbox/` & `numax/guardian/`: The execution safety layers. Validates tool permissions against current `AutonomyMode`. If a tool crosses a risk threshold, the `pre_tool_use` hook traps it.
- `numax/action/` & `numax/artifacts/`: Instead of strings, NUMAX generates Pydantic `Artifacts` (code, specs, reports) validated by schema before delivery.

### 4. Extensions & Scalability
- `numax/subagents/`: Independent routines with bounded parameters (budget, autonomy) spawned by the core to solve isolated logic.
- `numax/recipes/`: JSON-loadable deterministic workflows.
- `numax/providers/` & `numax/models/`: The interchangeable LLM layer mapping capability and roles (critic vs architect) to specific APIs (Google, Anthropic, Mock).

### 5. API & Export
- `numax/server/`: The asynchronous FastAPI backend. Exposes the NUMAX library over HTTP for 24/7 autonomous behavior.
- `numax/mcp/`: Exposes NUMAX tools and memory dynamically to compatible local systems (e.g. IDEs like Cursor/Claude) via the Model Context Protocol.

### 6. Observability
- `numax/obs/`: Emits flat `.jsonl` traces for every edge traversal and node decision.
- `numax/session/` & `numax/identity/`: Every boot calculates a `RuntimeIdentity` hash. Every execution exports a post-mortem diagnostic block.

## The FSM Rhythm
Every interaction generally follows:
`PERCEIVE (Input)` → `ROUTE (Intent)` → `RETRIEVE (Context)` → `PLAN (Morsels)` → `EXECUTE (Tools)` → `CRITICIZE (Validation)` → `DELIVER (Artifact)`

At any point, the **Kill Switch** (`numax/guardian/kill_switch.py`) can interrupt the FSM if safety, confidence, or tokens deplete below defined thresholds.
