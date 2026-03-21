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
from numax.flows.basic_chat import build_basic_chat_flow
from numax.flows.planning_execution import build_planning_execution_flow
from numax.flows.retrieval_answer import build_retrieval_answer_flow
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
    elif flow == "retrieval_answer":
        graph = build_retrieval_answer_flow()
        start = "intent_router"
    elif flow == "planning_execution":
        graph = build_planning_execution_flow()
        start = "intent_router"
    elif flow == "artifact_output":
        graph = build_artifact_output_flow()
        start = "intent_router"
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
            f"{spec.name} risk={spec.risk_level} confirm={spec.requires_confirmation} tags={spec.tags}"
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


if __name__ == "__main__":
    app()
