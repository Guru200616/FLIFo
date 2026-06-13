from __future__ import annotations

import ast
import hashlib
import re
from pathlib import Path
from acia.core.repository import EXTENSION_LANGUAGE, iter_source_files
from acia.models.schemas import CodeChunk, CodeSymbol


def _chunk_id(repo: str, file_path: str, name: str, line: int) -> str:
    return hashlib.sha256(f"{repo}:{file_path}:{name}:{line}".encode()).hexdigest()[:16]


def parse_python(path: Path, repo_root: Path) -> tuple[list[CodeSymbol], list[CodeChunk]]:
    text = path.read_text(errors="ignore")
    rel = str(path.relative_to(repo_root))
    tree = ast.parse(text or "\n")
    lines = text.splitlines()
    symbols, chunks = [], []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            kind = "class" if isinstance(node, ast.ClassDef) else "function"
            end = getattr(node, "end_lineno", node.lineno)
            content = "\n".join(lines[node.lineno - 1:end])
            symbols.append(CodeSymbol(name=node.name, kind=kind, file_path=rel, line_start=node.lineno, line_end=end))
            chunks.append(CodeChunk(id=_chunk_id("local", rel, node.name, node.lineno), repository_id="local", file_path=rel, language="Python", symbol=node.name, kind=kind, content=content, start_line=node.lineno, end_line=end))
    return symbols, chunks


def parse_text_symbols(path: Path, repo_root: Path) -> tuple[list[CodeSymbol], list[CodeChunk]]:
    text = path.read_text(errors="ignore")
    rel = str(path.relative_to(repo_root))
    language = EXTENSION_LANGUAGE.get(path.suffix, "Text")
    symbols, chunks = [], []
    pattern = re.compile(r"^\s*(?:export\s+)?(?:async\s+)?(?:function|class)\s+([A-Za-z_$][\w$]*)|^\s*(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?\(", re.M)
    lines = text.splitlines()
    for match in pattern.finditer(text):
        name = match.group(1) or match.group(2)
        line = text[: match.start()].count("\n") + 1
        end = min(len(lines), line + 80)
        kind = "class" if "class" in match.group(0) else "function"
        content = "\n".join(lines[line - 1:end])
        symbols.append(CodeSymbol(name=name, kind=kind, file_path=rel, line_start=line, line_end=end))
        chunks.append(CodeChunk(id=_chunk_id("local", rel, name, line), repository_id="local", file_path=rel, language=language, symbol=name, kind=kind, content=content, start_line=line, end_line=end))
    if not chunks and text.strip():
        chunks.append(CodeChunk(id=_chunk_id("local", rel, "module", 1), repository_id="local", file_path=rel, language=language, content=text[:12000], start_line=1, end_line=len(lines)))
    return symbols, chunks


def parse_repository(root: Path) -> tuple[list[CodeSymbol], list[CodeChunk]]:
    all_symbols, all_chunks = [], []
    for path in iter_source_files(root):
        symbols, chunks = parse_python(path, root) if path.suffix == ".py" else parse_text_symbols(path, root)
        all_symbols.extend(symbols); all_chunks.extend(chunks)
    return all_symbols, all_chunks
