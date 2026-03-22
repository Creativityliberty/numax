from __future__ import annotations

import uuid

import typer
import uvicorn

from benchmarks.report import save_report
from benchmarks.runner import run_benchmarks
from numax.bootstrap import build_model_catalog, build_provider_registry
from numax.configs.loader import (
    get_budget_limits,
    get_runtime_autonomy_mode,
    load_config,
)
from numax.core.state import NumaxState
from numax.flows.artifact_output import build_artifact_output_flow
from numax.flows.blackboard_cycle import build_blackboard_cycle_flow
from numax.flows.catalog_sync import build_catalog_sync_flow
from numax.flows.basic_chat import build_basic_chat_flow
from numax.flows.planning_execution import build_planning_execution_flow
from numax.flows.retrieval_answer import build_retrieval_answer_flow
from numax.flows.workspace_analysis import build_workspace_analysis_flow
from numax.flows.workspace_search import build_workspace_search_flow
from numax.flows.code_change_loop import build_code_change_loop_flow
from numax.flows.director_orchestration import build_director_orchestration_flow
from numax.flows.team_run import build_team_run_flow
from numax.flows.team_batch_run import run_team_batch
from numax.flows.team_map_reduce import run_team_map_reduce
from numax.flows.repo_repair import build_repo_repair_flow
from numax.flows.subagent_review import build_subagent_review_flow
from numax.flows.specification_loop import build_specification_loop_flow
from numax.flows.improvement_loop import build_improvement_loop_flow
from numax.flows.profile_apply import build_profile_apply_flow
from numax.flows.runtime_resilience import build_runtime_resilience_flow
from numax.flows.recipe_run import build_recipe_run_flow
from numax.flows.external_subagent_run import build_external_subagent_run_flow
from numax.flows.learning_feedback import build_learning_feedback_flow
from numax.teams.blackboard import BlackboardState, list_blackboard_entries
from numax.catalog.registry import build_catalog_registry
from numax.learning.mode_feedback import load_mode_feedback
from numax.learning.mode_stats import compute_mode_stats
from numax.learning.mode_selector import select_best_mode
from numax.teams.registry import build_default_team_registry
from numax.jobs.retry_scheduler import schedule_retry
from numax.packs.install import install_pack
from numax.packs.registry import build_default_pack_registry
from numax.health.startup_checks import run_startup_checks
from numax.identity.runtime_identity import build_runtime_identity
from numax.learning.critic_calibration import load_critic_policy
from numax.learning.model_selector import load_model_selector_policy
from numax.learning.policy_feedback import apply_feedback
from numax.learning.retrieval_ranker import load_ranker_policy
from numax.learning.router import load_router_policy
from numax.memory.continuity import restore_continuity, save_continuity_state
from numax.obs.traces import save_run_trace
from numax.session.diagnostics import build_session_diagnostics
from numax.tools.default_tools import build_default_tool_registry

app = typer.Typer()


@app.command("hello")
def hello_cmd() -> None:
    print("NUMAX CLI IS ALIVE")


@app.command()
def run(
    flow: str = typer.Option("basic_chat", help="Flow name"),
    prompt: str = typer.Option(..., help="User input"),
    continuity_path: str = typer.Option("data/state/continuity.json", help="Continuity file"),
    restore: bool = typer.Option(False, help="Restore previous continuity state"),
    save: bool = typer.Option(True, help="Save continuity state after run"),
) -> None:
    config = load_config()
    budget_cfg = get_budget_limits(config)

    state = NumaxState(
        observation={"raw_input": prompt},
    )
    state.runtime.run_id = str(uuid.uuid4())
    state.budget.max_tokens_total = budget_cfg["max_tokens_total"]
    state.budget.max_cost_usd = budget_cfg["max_cost_usd"]
    state.world_state["autonomy_mode"] = get_runtime_autonomy_mode(config)
    state.world_state["artifact_type"] = "summary"
    state.world_state["artifact_title"] = "NUMAX Generated Artifact"

    if restore:
        state = restore_continuity(state, continuity_path)

    if flow == "basic_chat":
        graph = build_basic_chat_flow()
        start = "intent_router"
    elif flow == "blackboard_cycle":
        graph = build_blackboard_cycle_flow()
        start = "blackboard_publish"
    elif flow == "catalog_sync":
        graph = build_catalog_sync_flow()
        start = "catalog_sync"
    elif flow == "director_orchestration":
        graph = build_director_orchestration_flow()
        start = "director_plan"
    elif flow == "retrieval_answer":
        graph = build_retrieval_answer_flow()
        start = "intent_router"
    elif flow == "planning_execution":
        graph = build_planning_execution_flow()
        start = "intent_router"
    elif flow == "artifact_output":
        graph = build_artifact_output_flow()
        start = "intent_router"
    elif flow == "workspace_analysis":
        graph = build_workspace_analysis_flow()
        start = "workspace_open"
    elif flow == "workspace_search":
        graph = build_workspace_search_flow()
        start = "workspace_open"
    elif flow == "code_change_loop":
        graph = build_code_change_loop_flow()
        start = "workspace_open"
    elif flow == "repo_repair":
        graph = build_repo_repair_flow()
        start = "workspace_open"
    elif flow == "team_run":
        graph = build_team_run_flow()
        start = "team_load"
    elif flow == "subagent_review":
        graph = build_subagent_review_flow()
        start = "subagent_orchestrate"
    elif flow == "specification_loop":
        graph = build_specification_loop_flow()
        start = "intent_spec"
    elif flow == "improvement_loop":
        graph = build_improvement_loop_flow()
        start = "improvement_loop"
    elif flow == "profile_apply":
        graph = build_profile_apply_flow()
        start = "profile_apply"
    elif flow == "runtime_resilience":
        graph = build_runtime_resilience_flow()
        start = "runtime_collect_events"
    elif flow == "recipe_run":
        graph = build_recipe_run_flow()
        start = "recipe_apply"
    elif flow == "external_subagent_run":
        graph = build_external_subagent_run_flow()
        start = "external_subagent"
    elif flow == "learning_feedback_loop":
        graph = build_learning_feedback_flow()
        start = "learning_feedback"
    else:
        raise typer.BadParameter(f"Unsupported flow: {flow}")

    final_state = graph.run(start=start, state=state)

    if save:
        save_continuity_state(final_state, continuity_path)

    trace_path = save_run_trace(final_state)
    diagnostics = build_session_diagnostics(final_state)

    typer.echo("=== FINAL OUTPUT ===")
    typer.echo(final_state.final_output)

    typer.echo("\n=== ARTIFACT ===")
    typer.echo(final_state.world_state.get("artifact"))

    typer.echo("\n=== DIAGNOSTICS ===")
    typer.echo(diagnostics)

    typer.echo("\n=== TRACE FILE ===")
    typer.echo(trace_path)


@app.command("providers-list")
def providers_list() -> None:
    registry = build_provider_registry()
    for name in registry.list_providers():
        typer.echo(name)


@app.command("models-list")
def models_list() -> None:
    catalog = build_model_catalog()
    for model in catalog.all():
        typer.echo(f"{model.id} roles={model.roles} capabilities={model.capabilities}")


@app.command("tools-list")
def tools_list() -> None:
    registry = build_default_tool_registry()
    for spec in registry.list_tools():
        typer.echo(
            f"{spec.name} risk={spec.risk_level} "
            f"confirm={spec.requires_confirmation} tags={spec.tags}"
        )


@app.command("mcp-capabilities")
def mcp_capabilities() -> None:
    from numax.mcp.server import mcp

    typer.echo(f"MCP Server initialized: {mcp.name}")


@app.command("runtime-identity")
def runtime_identity() -> None:
    typer.echo(build_runtime_identity())


@app.command("startup-checks")
def startup_checks() -> None:
    result = run_startup_checks()
    typer.echo({"ok": result.ok, "notes": result.notes})


@app.command("config-show")
def config_show() -> None:
    typer.echo(load_config())


@app.command("learning-show")
def learning_show() -> None:
    typer.echo(
        {
            "router": load_router_policy(),
            "model_selector": load_model_selector_policy(),
            "retrieval_ranker": load_ranker_policy(),
            "critic": load_critic_policy(),
        }
    )


@app.command("feedback-apply")
def feedback_apply(
    target: str = typer.Option(...),
    key: str = typer.Option(None),
    value: str = typer.Option(None),
) -> None:
    feedback = {"target": target}
    if key is not None:
        feedback[key] = value
    typer.echo(apply_feedback(feedback))


@app.command("benchmark-run")
def benchmark_run() -> None:
    report = run_benchmarks()
    paths = save_report(report)

    typer.echo("=== BENCHMARK SUMMARY ===")
    typer.echo(report["summary"])

    typer.echo("\n=== REPORT FILES ===")
    typer.echo(paths)


@app.command("serve")
def serve(
    host: str = typer.Option("127.0.0.1"),
    port: int = typer.Option(8000),
) -> None:
    uvicorn.run("numax.server.app:app", host=host, port=port, reload=True)


@app.command("skills-list")
def skills_list() -> None:
    from numax.skills.registry import build_default_skill_registry

    registry = build_default_skill_registry()
    for skill_id in registry.list_ids():
        skill = registry.get(skill_id)
        typer.echo(f"- {skill_id} (v{skill.version}): {skill.title}")


@app.command("skill-apply")
def skill_apply_cmd(
    skill_id: str = typer.Option(...),
    preview: bool = typer.Option(True),
) -> None:
    from numax.skills.apply import apply_skill

    result = apply_skill(skill_id, preview=preview)
    typer.echo(f"OK: {result.ok} Preview: {result.preview} Notes: {result.notes}")


@app.command("skill-uninstall")
def skill_uninstall_cmd(
    skill_id: str = typer.Option(...),
) -> None:
    from numax.skills.uninstall import uninstall_skill

    result = uninstall_skill(skill_id)
    typer.echo(f"OK: {result.ok} Notes: {result.notes}")


@app.command("skill-replay")
def skill_replay_cmd() -> None:
    from numax.skills.replay import replay_skills

    result = replay_skills()
    typer.echo(f"OK: {result.ok} Notes: {result.notes}")


@app.command("async-providers-list")
def async_providers_list() -> None:
    from numax.providers.async_bootstrap import build_async_provider_registry

    registry = build_async_provider_registry()
    typer.echo(registry.list_providers())


@app.command("store-backend")
def store_backend() -> None:
    from numax.storage.bootstrap import build_default_store
    
    store = build_default_store()
    typer.echo(type(store).__name__)


@app.command("jobs-list")
def jobs_list() -> None:
    from numax.jobs.repo import JobRepository
    from numax.storage.bootstrap import build_default_store

    repo = JobRepository(build_default_store())
    typer.echo(repo.list_all())


@app.command("spans-tail")
def spans_tail() -> None:
    from pathlib import Path

    path = Path("data/traces/spans.jsonl")
    if not path.exists():
        typer.echo([])
        return
    lines = path.read_text(encoding="utf-8").splitlines()[-10:]
    typer.echo(lines)


@app.command("whoami-local")
def whoami_local() -> None:
    from numax.auth.context import build_local_admin_context

    typer.echo(build_local_admin_context())


@app.command("sandbox-echo")
def sandbox_echo(message: str = typer.Option("hello")) -> None:
    from numax.guardian.enforcer import enforce_sandbox_command

    typer.echo(
        enforce_sandbox_command(
            user_roles=["admin"],
            command=["echo", message],
        )
    )


@app.command("workspace-scan")
def workspace_scan(
    path: str = typer.Option(".", help="Workspace path"),
    project_name: str = typer.Option(None, help="Optional project name"),
) -> None:
    state = NumaxState(
        observation={
            "workspace_path": path,
            "project_name": project_name,
        }
    )
    state.runtime.run_id = str(uuid.uuid4())

    graph = build_workspace_analysis_flow()
    final_state = graph.run(start="workspace_open", state=state)

    typer.echo(final_state.final_output)


@app.command("workspace-search")
def workspace_search(
    path: str = typer.Option(".", help="Workspace path"),
    query: str = typer.Option(..., help="Search query"),
) -> None:
    state = NumaxState(
        observation={
            "workspace_path": path,
            "search_query": query,
        }
    )
    state.runtime.run_id = str(uuid.uuid4())

    graph = build_workspace_search_flow()
    final_state = graph.run(start="workspace_open", state=state)

    typer.echo(final_state.world_state.get("workspace_search"))


@app.command("workspace-repair")
def workspace_repair(
    path: str = typer.Option(".", help="Workspace path"),
    query: str = typer.Option(..., help="Search query"),
    patch_old_text: str = typer.Option(None, help="Old text to replace"),
    patch_new_text: str = typer.Option(None, help="New text"),
    preview_patch: bool = typer.Option(True, help="Preview only"),
) -> None:
    state = NumaxState(
        observation={
            "workspace_path": path,
            "search_query": query,
            "patch_old_text": patch_old_text,
            "patch_new_text": patch_new_text,
            "preview_patch": preview_patch,
        }
    )
    state.runtime.run_id = str(uuid.uuid4())

    graph = build_repo_repair_flow()
    final_state = graph.run(start="workspace_open", state=state)

    typer.echo(
        {
            "workspace": final_state.active_workspace,
            "active_files": final_state.active_files,
            "last_patch": final_state.last_patch,
            "last_test_run": final_state.last_test_run,
            "code_review": final_state.world_state.get("code_review"),
            "patch_risk": final_state.patch_risk,
            "change_scope": final_state.change_scope,
            "last_failure": final_state.last_failure,
            "next_recommended_action": final_state.next_recommended_action,
        }
    )


@app.command("subagent-review")
def subagent_review(
    path: str = typer.Option(".", help="Workspace path"),
    query: str = typer.Option("", help="Optional search query"),
) -> None:
    state = NumaxState(
        observation={
            "workspace_path": path,
            "search_query": query,
        }
    )
    state.runtime.run_id = str(uuid.uuid4())

    graph = build_subagent_review_flow()
    final_state = graph.run(start="subagent_orchestrate", state=state)

    typer.echo(
        {
            "active_subagent": final_state.active_subagent,
            "subagent_plan": final_state.subagent_plan,
            "subagent_notes": final_state.subagent_notes,
            "next_recommended_action": final_state.next_recommended_action,
        }
    )


@app.command("spec-run")
def spec_run(
    prompt: str = typer.Option(..., help="Raw task input"),
) -> None:
    state = NumaxState(
        observation={
            "raw_input": prompt,
        }
    )
    state.runtime.run_id = str(uuid.uuid4())

    graph = build_specification_loop_flow()
    final_state = graph.run(start="intent_spec", state=state)

    typer.echo(
        {
            "intent_spec": final_state.intent_spec,
            "assumptions": final_state.assumptions,
            "work_spec": final_state.work_spec,
            "spec_status": final_state.spec_status,
            "next_recommended_action": final_state.next_recommended_action,
            "validation": final_state.world_state.get("spec_validation"),
        }
    )


@app.command("improve-run")
def improve_run(
    safety_confidence: float = typer.Option(1.0, help="Safety confidence"),
    degraded: bool = typer.Option(False, help="Whether runtime is degraded"),
    retries: int = typer.Option(0, help="Current retry count"),
    test_failed: bool = typer.Option(False, help="Whether the latest test failed"),
    review_decision: str = typer.Option("", help="Code review decision"),
) -> None:
    state = NumaxState()
    state.runtime.run_id = str(uuid.uuid4())
    state.runtime.degraded = degraded
    state.runtime.retries = retries
    state.confidence.safety_confidence = safety_confidence

    if test_failed:
        state.last_test_run = {"ok": False}
        state.last_failure = {"kind": "test_failure"}

    if review_decision:
        state.world_state["code_review"] = {
            "decision": review_decision,
            "risk": "medium",
            "scope": "medium",
            "notes": ["Injected review decision from CLI."],
        }

    graph = build_improvement_loop_flow()
    final_state = graph.run(start="improvement_loop", state=state)

    typer.echo(
        {
            "improvement_suggestions": final_state.improvement_suggestions,
            "retry_decision": final_state.retry_decision,
            "mutation_decision": final_state.mutation_decision,
            "improvement_status": final_state.improvement_status,
            "next_recommended_action": final_state.next_recommended_action,
        }
    )


@app.command("profiles-list")
def profiles_list() -> None:
    from numax.profiles.registry import build_default_profile_registry
    registry = build_default_profile_registry()
    for profile_id in registry.list_ids():
        profile = registry.get(profile_id)
        typer.echo(f"{profile.profile_id} - {profile.title}")


@app.command("profile-apply")
def profile_apply_cmd(
    profile_id: str = typer.Option(..., help="Profile identifier"),
    preview: bool = typer.Option(True, help="Preview only"),
) -> None:
    from numax.profiles.apply import apply_profile
    result = apply_profile(profile_id=profile_id, preview=preview)
    typer.echo(
        {
            "ok": result.ok,
            "profile_id": result.profile_id,
            "notes": result.notes,
        }
    )


@app.command("runtime-check")
def runtime_check(
    flow_name: str = typer.Option("basic_chat", help="Flow name"),
    degraded: bool = typer.Option(False, help="Whether runtime is degraded"),
) -> None:
    state = NumaxState()
    state.runtime.run_id = str(uuid.uuid4())
    state.runtime.flow_name = flow_name
    state.runtime.degraded = degraded

    state.world_state["runtime_events"] = [
        {"kind": "trace", "name": "flow_started", "payload": {}, "severity": "info"},
        {"kind": "provider", "name": "provider_attempt", "payload": {"provider": "mock"}, "severity": "info"},
        {"kind": "sdk_weird_unknown_kind", "name": "weird_event", "payload": {"x": 1}, "severity": "warning"},
    ]

    graph = build_runtime_resilience_flow()
    final_state = graph.run(start="runtime_collect_events", state=state)

    typer.echo(
        {
            "runtime_events": final_state.runtime_events,
            "event_buffer_status": final_state.event_buffer_status,
            "timeout_decision": final_state.timeout_decision,
            "runtime_resilience_status": final_state.runtime_resilience_status,
            "next_recommended_action": final_state.next_recommended_action,
        }
    )


@app.command("recipes-list")
def recipes_list() -> None:
    from numax.recipes.registry import build_default_recipe_registry
    registry = build_default_recipe_registry()
    for recipe_id in registry.list_ids():
        recipe = registry.get(recipe_id)
        typer.echo(f"{recipe.recipe_id} - {recipe.title} -> flow={recipe.flow}")


@app.command("recipe-apply")
def recipe_apply_cmd(
    recipe_id: str = typer.Option(..., help="Recipe identifier"),
    preview: bool = typer.Option(True, help="Preview only"),
) -> None:
    from numax.recipes.apply import apply_recipe
    result = apply_recipe(recipe_id=recipe_id, preview=preview)
    typer.echo(
        {
            "ok": result.ok,
            "recipe_id": result.recipe_id,
            "execution_plan": result.execution_plan,
            "notes": result.notes,
        }
    )


@app.command("recipe-run")
def recipe_run_cmd(
    recipe_id: str = typer.Option(..., help="Recipe identifier"),
    preview: bool = typer.Option(True, help="Preview only"),
) -> None:
    state = NumaxState(
        observation={
            "recipe_id": recipe_id,
            "recipe_preview": preview,
        }
    )
    state.runtime.run_id = str(uuid.uuid4())

    graph = build_recipe_run_flow()
    final_state = graph.run(start="recipe_apply", state=state)

    typer.echo(
        {
            "active_recipe": final_state.active_recipe,
            "recipe_apply_result": final_state.recipe_apply_result,
            "next_recommended_action": final_state.next_recommended_action,
            "execution_plan": final_state.world_state.get("recipe_execution_plan"),
        }
    )


@app.command("external-subagents-list")
def external_subagents_list() -> None:
    from numax.subagents.external import build_default_external_subagent_registry
    registry = build_default_external_subagent_registry()
    typer.echo(registry.list_ids())


@app.command("external-subagent-run")
def external_subagent_run_cmd(
    subagent_id: str = typer.Option("mock_repo_worker", help="External subagent identifier"),
    mode: str = typer.Option("read_only", help="Invocation mode"),
    prompt: str = typer.Option("Inspect the repo task", help="Task prompt"),
) -> None:
    state = NumaxState(
        observation={
            "raw_input": prompt,
            "external_subagent_id": subagent_id,
            "external_subagent_mode": mode,
            "user_roles": ["admin"],
        }
    )
    state.runtime.run_id = str(uuid.uuid4())

    graph = build_external_subagent_run_flow()
    final_state = graph.run(start="external_subagent", state=state)

    typer.echo(
        {
            "external_subagent_result": final_state.external_subagent_result,
            "next_recommended_action": final_state.next_recommended_action,
        }
    )


@app.command("learning-stats")
def learning_stats_cmd() -> None:
    from numax.learning.mode_stats import ModeStatsAggregator, build_mock_history
    # Mock history for now
    aggregator = ModeStatsAggregator(history=build_mock_history())
    typer.echo(aggregator.get_all_summaries())


@app.command("learning-recommend")
def learning_recommend_cmd(
    task_type: str = typer.Option("general", help="Task type"),
    candidates: str = typer.Option("repo_operator,research_mode", help="Comma-separated candidates"),
) -> None:
    from numax.learning.mode_selector import SmartModeSelector
    from numax.learning.mode_stats import build_mock_history
    
    candidate_list = [c.strip() for c in candidates.split(",")]
    selector = SmartModeSelector(history=build_mock_history())
    recommendation = selector.recommend(task_type=task_type, candidates=candidate_list)
    
    typer.echo(recommendation)


@app.command("learning-run")
def learning_run_cmd(
    recipe_id: str = typer.Option("workspace_audit", help="Recipe to run and learn from"),
) -> None:
    state = NumaxState(
        observation={
            "recipe_id": recipe_id,
        }
    )
    state.runtime.run_id = str(uuid.uuid4())
    state.active_recipe = recipe_id

    graph = build_learning_feedback_flow()
    final_state = graph.run(start="learning_feedback", state=state)

    typer.echo(
        {
            "active_feedback": final_state.active_feedback,
            "mode_recommendation": final_state.mode_recommendation,
            "next_recommended_action": final_state.next_recommended_action,
        }
    )


@app.command("mode-feedback-show")
def mode_feedback_show() -> None:
    typer.echo(load_mode_feedback())


@app.command("mode-stats")
def mode_stats_cmd(
    group_by: str = typer.Option("profile", help="profile or recipe"),
) -> None:
    typer.echo(compute_mode_stats(group_by=group_by))


@app.command("mode-select")
def mode_select_cmd(
    group_by: str = typer.Option("profile", help="profile or recipe"),
    min_runs: int = typer.Option(1, help="Minimum number of runs"),
) -> None:
    typer.echo(select_best_mode(group_by=group_by, min_runs=min_runs))


@app.command("packs-list")
def packs_list() -> None:
    registry = build_default_pack_registry()
    typer.echo(registry.list_ids())


@app.command("pack-install")
def pack_install(pack_id: str = typer.Option(...)) -> None:
    typer.echo(install_pack(pack_id))


@app.command("retry-schedule")
def retry_schedule(job_id: str = typer.Option("job-1"), retries: int = typer.Option(0)) -> None:
    typer.echo(schedule_retry(job_id=job_id, retries=retries))


@app.command("teams-list")
def teams_list() -> None:
    registry = build_default_team_registry()
    for team_id in registry.list_ids():
        team = registry.get(team_id)
        typer.echo(f"{team.team_id} - {team.name} -> flow={team.default_flow}")


@app.command("team-run")
def team_run_cmd(
    team_id: str = typer.Option("product_squad", help="Team identifier"),
    prompt: str = typer.Option("Prepare a mission", help="Mission objective"),
) -> None:
    state = NumaxState(
        observation={
            "team_id": team_id,
            "raw_input": prompt,
        }
    )
    state.runtime.run_id = str(uuid.uuid4())

    graph = build_team_run_flow()
    final_state = graph.run(start="team_load", state=state)

    typer.echo(
        {
            "teams_state": final_state.teams_state,
            "team_results": final_state.team_results,
            "next_recommended_action": final_state.next_recommended_action,
        }
    )


@app.command("team-handover-check")
def team_handover_check(
    from_team: str = typer.Option("product_squad"),
    to_team: str = typer.Option("engineering_squad"),
    artifact_type: str = typer.Option("spec"),
    objective: str = typer.Option("Build the implementation"),
) -> None:
    from numax.teams.handover import validate_handover

    payload = {"objective": objective}
    result = validate_handover(
        from_team=from_team,
        to_team=to_team,
        artifact_type=artifact_type,
        payload=payload,
    )
    typer.echo(result.model_dump())


@app.command("blackboard-publish")
def blackboard_publish_cmd(
    team_id: str = typer.Option("product_squad"),
    artifact_type: str = typer.Option("spec"),
    objective: str = typer.Option("Build the implementation"),
    consume_team_id: str = typer.Option("engineering_squad"),
) -> None:
    state = NumaxState(
        observation={
            "team_id": team_id,
            "artifact_type": artifact_type,
            "artifact_payload": {"objective": objective},
            "consume_team_id": consume_team_id,
        }
    )
    state.runtime.run_id = str(uuid.uuid4())

    graph = build_blackboard_cycle_flow()
    final_state = graph.run(start="blackboard_publish", state=state)

    typer.echo(
        {
            "blackboard_state": final_state.blackboard_state,
            "mission_queue": final_state.mission_queue,
            "subscription_state": final_state.subscription_state,
            "next_recommended_action": final_state.next_recommended_action,
        }
    )


@app.command("blackboard-show")
def blackboard_show(
    artifact_type: str = typer.Option(None),
) -> None:
    state = BlackboardState(entries=[])
    typer.echo(list_blackboard_entries(state, artifact_type=artifact_type))


@app.command("team-batch-run")
def team_batch_run_cmd() -> None:
    base_state = NumaxState()

    batch_inputs = [
        {"team_id": "product_squad", "raw_input": "Prepare product spec"},
        {"team_id": "engineering_squad", "raw_input": "Implement repo patch"},
        {"team_id": "qa_squad", "raw_input": "Review patch quality"},
    ]

    results = run_team_batch(base_state=base_state, batch_inputs=batch_inputs)
    typer.echo(results)


@app.command("team-map-reduce")
def team_map_reduce_cmd() -> None:
    base_state = NumaxState()

    missions = [
        {"team_id": "product_squad", "raw_input": "Define V3 mission"},
        {"team_id": "engineering_squad", "raw_input": "Implement V3 module"},
        {"team_id": "qa_squad", "raw_input": "Audit V3 output"},
    ]

    result = run_team_map_reduce(base_state=base_state, missions=missions)
    typer.echo(result)


@app.command("catalog-sync")
def catalog_sync_cmd() -> None:
    state = NumaxState()
    state.runtime.run_id = str(uuid.uuid4())

    graph = build_catalog_sync_flow()
    final_state = graph.run(start="catalog_sync", state=state)

    typer.echo(
        {
            "catalog_sync_result": final_state.catalog_sync_result,
            "catalog_team_templates": final_state.catalog_team_templates,
            "next_recommended_action": final_state.next_recommended_action,
        }
    )


@app.command("catalog-show")
def catalog_show() -> None:
    typer.echo(build_catalog_registry())


@app.command("director-run")
def director_run_cmd(
    prompt: str = typer.Option("Build NUMAX V3 multi-team architecture", help="Global objective"),
) -> None:
    state = NumaxState(
        observation={
            "raw_input": prompt,
        }
    )
    state.runtime.run_id = str(uuid.uuid4())

    graph = build_director_orchestration_flow()
    final_state = graph.run(start="director_plan", state=state)

    typer.echo(
        {
            "director_plan": final_state.director_plan,
            "director_assignments": final_state.director_assignments,
            "director_results": final_state.director_results,
            "next_recommended_action": final_state.next_recommended_action,
        }
    )


if __name__ == "__main__":
    app()
