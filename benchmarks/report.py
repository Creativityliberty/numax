from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def render_markdown_report(report: dict[str, Any]) -> str:
    lines = ["# NUMAX Benchmark Report", ""]

    summary = report.get("summary", {})
    for system, metrics in summary.items():
        lines.append(f"## {system}")
        for key, value in metrics.items():
            lines.append(f"- **{key}**: {value}")
        lines.append("")

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
