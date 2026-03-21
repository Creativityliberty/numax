from __future__ import annotations

from typing import Any, Dict

from numax.tools.file_reader import read_file
from numax.tools.file_writer import write_file
from numax.tools.search_code import search_code
from numax.tools.git_diff import get_git_diff
from numax.tools.test_runner import run_tests


class WorkspaceTools:
    def read(self, path: str) -> Dict[str, Any]:
        return read_file(path)

    def write(self, path: str, content: str, overwrite: bool = False) -> Dict[str, Any]:
        return write_file(path=path, content=content, overwrite=overwrite)

    def search(self, root_path: str, query: str, max_results: int = 50) -> Dict[str, Any]:
        return search_code(root_path=root_path, query=query, max_results=max_results)

    def diff(self, root_path: str, staged: bool = False) -> Dict[str, Any]:
        return get_git_diff(root_path=root_path, staged=staged)

    def test(self, root_path: str, command: list[str] | None = None) -> Dict[str, Any]:
        return run_tests(root_path=root_path, command=command)
