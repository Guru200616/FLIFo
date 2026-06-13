from __future__ import annotations

from pathlib import Path
from acia.core.parser import parse_repository


def summarize_repository(root: Path) -> dict[str, object]:
    symbols, chunks = parse_repository(root)
    files = sorted({chunk.file_path for chunk in chunks})
    modules: dict[str, list[str]] = {}
    for symbol in symbols:
        modules.setdefault(symbol.file_path, []).append(f"{symbol.kind} {symbol.name}")
    return {
        "file_summaries": {path: f"Contains {len(modules.get(path, []))} indexed symbols." for path in files},
        "module_summaries": modules,
        "repository_summary": f"Indexed {len(files)} files with {len(symbols)} symbols across the repository.",
    }
