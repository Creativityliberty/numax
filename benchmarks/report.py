from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def render_markdown_report(report: dict[str, Any]) -> str:
    lines = ["# NUMAX Benchmark Report", ""]

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
            f"tokens={row.get('tokens_used')} "
            f"cost={row.get('cost_used_usd')}"
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
