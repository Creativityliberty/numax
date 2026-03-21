from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class IndexedFile(BaseModel):
    path: str
    kind: str = "unknown"  # code, config, doc, test, data
    size_bytes: int = 0
    language: Optional[str] = None
    important: bool = False
    tags: List[str] = Field(default_factory=list)


class FileIndex(BaseModel):
    root_path: str
    files: List[IndexedFile] = Field(default_factory=list)
