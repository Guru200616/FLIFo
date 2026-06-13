from __future__ import annotations

from pathlib import Path
from codesage_ai.agents.graph import build_import_graph, impacted_by
from codesage_ai.agents.retrieval import bm25_search
from codesage_ai.agents.security import scan_repository
from codesage_ai.core.parser import parse_repository
from codesage_ai.core.repository import detect_frameworks, detect_languages
from codesage_ai.models.schemas import ChatAnswer, ImpactReport, RepositoryOverview


class RepositoryIntelligenceOrchestrator:
    """MVP orchestration facade; designed to be replaced by LangGraph nodes in production."""

    def analyze(self, root: Path) -> RepositoryOverview:
        symbols, _ = parse_repository(root)
        frameworks = detect_frameworks(root)
        pattern = "frontend-backend" if {"react", "fastapi", "express"} & set(frameworks) else "modular"
        return RepositoryOverview(repository_id="local", root=root, languages=detect_languages(root), frameworks=frameworks, architecture_pattern=pattern, files_indexed=len({s.file_path for s in symbols}), symbols=symbols)

    def answer(self, root: Path, question: str) -> ChatAnswer:
        _, chunks = parse_repository(root)
        hits = bm25_search(question, chunks)
        citations = [f"{c.file_path}:{c.start_line}-{c.end_line}" for c in hits]
        summary = "\n".join(f"- {c.file_path}::{c.symbol or c.kind}: {c.content[:240].replace(chr(10), ' ')}" for c in hits[:5])
        return ChatAnswer(answer=f"Relevant repository context for: {question}\n{summary}", citations=citations)

    def security(self, root: Path):
        return scan_repository(root)

    def impact(self, root: Path, module: str) -> ImpactReport:
        graph = build_import_graph(root)
        affected = impacted_by(graph, module)
        return ImpactReport(changed_symbol=module, affected_modules=affected, affected_symbols=[], explanation="Modules importing the changed module are likely affected first; call graph expansion is planned for deeper impact analysis.")
