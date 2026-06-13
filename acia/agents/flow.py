from __future__ import annotations

from pathlib import Path
from acia.agents.retrieval import bm25_search
from acia.core.parser import parse_repository


def trace_execution_flow(root: Path, flow_name: str) -> dict[str, object]:
    _, chunks = parse_repository(root)
    hits = bm25_search(flow_name, chunks, limit=8)
    steps = [f"{chunk.file_path}:{chunk.start_line}-{chunk.end_line} handles {chunk.symbol or chunk.kind}" for chunk in hits]
    return {"flow": flow_name, "steps": steps, "references": [f"{c.file_path}:{c.start_line}" for c in hits]}
