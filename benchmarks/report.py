from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from numax.learning.mode_stats import compute_mode_stats


def render_markdown_report(report: dict[str, Any]) -> str:
    lines = ["# NUMAX Benchmark Report", ""]

    winner = report.get("winner")
    ranking = report.get("ranking", [])
    lines.append(f"**Winner:** {winner}")
    lines.append(f"**Ranking:** {ranking}")
    lines.append("")

    summary = report.get("summary", {})
    ordered_systems = sorted(summary.keys())

    for system in ordered_systems:
        metrics = summary[system]
        lines.append(f"## {system}")
        for key, value in metrics.items():
            lines.append(f"- **{key}**: {value}")
        lines.append("")

    lines.append("## Scenario Results")
    lines.append("")
    for row in report.get("results", []):
        lines.append(
            f"- `{row['system']}` on `{row['scenario_id']}` "
            f"=> success={row.get('task_success')} "
            f"artifact_valid={row.get('artifact_valid')} "
            f"recovered={row.get('recovered')} "
            f"continuity={row.get('continuity_score')} "
            f"rollback_ok={row.get('rollback_ok')} "
            f"replay_ok={row.get('replay_ok')} "
            f"tokens={row.get('tokens_used')} "
            f"cost={row.get('cost_used_usd')}"
        )

    mode_profile_stats = compute_mode_stats(group_by="profile")
    mode_recipe_stats = compute_mode_stats(group_by="recipe")

    lines.append("\n## Mode Profile Stats\n")
    for key, row in mode_profile_stats["stats"].items():
        lines.append(
            f"- {key}: success_rate={row['success_rate']:.2f}, "
            f"rollback_rate={row['rollback_rate']:.2f}, "
            f"avg_quality_score={row['avg_quality_score']:.2f}"
        )

    lines.append("\n## Mode Recipe Stats\n")
    for key, row in mode_recipe_stats["stats"].items():
        lines.append(
            f"- {key}: success_rate={row['success_rate']:.2f}, "
            f"rollback_rate={row['rollback_rate']:.2f}, "
            f"avg_quality_score={row['avg_quality_score']:.2f}"
        )

    return "\n".join(lines)


def save_report(report: dict[str, Any], output_dir: str = "benchmarks/outputs") -> dict[str, str]:
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)

    json_path = target / "benchmark_report.json"
    md_path = target / "benchmark_report.md"

    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown_report(report), encoding="utf-8")

    return {
        "json": str(json_path),
        "markdown": str(md_path),
    }
