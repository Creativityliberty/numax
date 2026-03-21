from __future__ import annotations

import uuid
from pathlib import Path
from typing import List

from numax.workspace.context import WorkspaceContext
from numax.workspace.file_index import FileIndex, IndexedFile
from numax.workspace.patchset import PatchSet
from numax.workspace.repo_state import RepoState


class WorkspaceService:
    def open_workspace(self, root_path: str, project_name: str | None = None) -> WorkspaceContext:
        root = Path(root_path).resolve()
        return WorkspaceContext(
            workspace_id=str(uuid.uuid4()),
            root_path=str(root),
            project_name=project_name or root.name,
        )

    def build_file_index(self, root_path: str, max_files: int = 200) -> FileIndex:
        root = Path(root_path).resolve()
        files: List[IndexedFile] = []

        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if ".git" in path.parts or "__pycache__" in path.parts:
                continue
                
            rel = str(path.relative_to(root))
            suffix = path.suffix.lower()

            kind = "unknown"
            language = None

            if suffix in {".py", ".ts", ".tsx", ".js", ".jsx", ".rs", ".go", ".java"}:
                kind = "code"
                language = suffix.lstrip(".")
            elif suffix in {".json", ".yaml", ".yml", ".toml", ".ini"}:
                kind = "config"
            elif suffix in {".md", ".txt"}:
                kind = "doc"
            elif "test" in rel.lower():
                kind = "test"

            files.append(
                IndexedFile(
                    path=rel,
                    kind=kind,
                    size_bytes=path.stat().st_size,
                    language=language,
                    important=rel in {"README.md", "pyproject.toml", "package.json"},
                )
            )

            if len(files) >= max_files:
                break

        return FileIndex(root_path=str(root), files=files)

    def empty_repo_state(self) -> RepoState:
        return RepoState()

    def create_patchset(self, workspace_id: str, rationale: str | None = None) -> PatchSet:
        return PatchSet(
            patch_id=str(uuid.uuid4()),
            workspace_id=workspace_id,
            rationale=rationale,
        )
