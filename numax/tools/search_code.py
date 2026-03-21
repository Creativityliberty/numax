from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List


DEFAULT_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".yaml", ".yml", ".md", ".toml"
}


def search_code(
    root_path: str,
    query: str,
    max_results: int = 50,
) -> Dict[str, Any]:
    root = Path(root_path).resolve()
    results: List[dict] = []

    if not root.exists():
        return {
            "ok": False,
            "error": "root_not_found",
            "root_path": str(root),
        }

    try:
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in DEFAULT_EXTENSIONS:
                continue

            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue

            for lineno, line in enumerate(text.splitlines(), start=1):
                if query.lower() in line.lower():
                    results.append(
                        {
                            "path": str(path.relative_to(root)),
                            "lineno": lineno,
                            "line": line.strip(),
                        }
                    )
                    if len(results) >= max_results:
                        return {
                            "ok": True,
                            "root_path": str(root),
                            "query": query,
                            "results": results,
                        }

        return {
            "ok": True,
            "root_path": str(root),
            "query": query,
            "results": results,
        }
    except Exception as exc:
        return {
            "ok": False,
            "error": str(exc),
            "root_path": str(root),
        }
