from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

try:
    from pydantic import BaseModel, Field, HttpUrl
except ModuleNotFoundError:
    PYDANTIC_AVAILABLE = False
    HttpUrl = str  # type: ignore[assignment]
else:
    PYDANTIC_AVAILABLE = True


class Severity(str, Enum):
    info = "info"
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


if PYDANTIC_AVAILABLE:
    class RepositoryIngestRequest(BaseModel):
        url: HttpUrl
        branch: str | None = None

    class CodeSymbol(BaseModel):
        name: str
        kind: str
        file_path: str
        line_start: int
        line_end: int
        signature: str | None = None

    class CodeChunk(BaseModel):
        id: str
        repository_id: str
        file_path: str
        language: str
        symbol: str | None = None
        kind: str = "module"
        content: str
        start_line: int
        end_line: int
        metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)

    class RepositoryOverview(BaseModel):
        repository_id: str
        root: Path
        languages: list[str]
        frameworks: list[str]
        architecture_pattern: str
        files_indexed: int
        symbols: list[CodeSymbol]

    class SecurityFinding(BaseModel):
        issue: str
        severity: Severity
        file_path: str
        line: int
        evidence: str
        recommendation: str

    class ImpactReport(BaseModel):
        changed_symbol: str
        affected_modules: list[str]
        affected_symbols: list[str]
        explanation: str

    class ChatAnswer(BaseModel):
        answer: str
        citations: list[str]
        execution_flow: list[str] = Field(default_factory=list)
else:
    @dataclass
    class RepositoryIngestRequest:
        url: HttpUrl
        branch: str | None = None

    @dataclass
    class CodeSymbol:
        name: str
        kind: str
        file_path: str
        line_start: int
        line_end: int
        signature: str | None = None

    @dataclass
    class CodeChunk:
        id: str
        repository_id: str
        file_path: str
        language: str
        symbol: str | None = None
        kind: str = "module"
        content: str = ""
        start_line: int = 1
        end_line: int = 1
        metadata: dict[str, str | int | float | bool] = field(default_factory=dict)

    @dataclass
    class RepositoryOverview:
        repository_id: str
        root: Path
        languages: list[str]
        frameworks: list[str]
        architecture_pattern: str
        files_indexed: int
        symbols: list[CodeSymbol]

    @dataclass
    class SecurityFinding:
        issue: str
        severity: Severity
        file_path: str
        line: int
        evidence: str
        recommendation: str

    @dataclass
    class ImpactReport:
        changed_symbol: str
        affected_modules: list[str]
        affected_symbols: list[str]
        explanation: str

    @dataclass
    class ChatAnswer:
        answer: str
        citations: list[str]
        execution_flow: list[str] = field(default_factory=list)
