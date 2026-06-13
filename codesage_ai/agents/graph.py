from __future__ import annotations

import ast
from pathlib import Path
import networkx as nx
from codesage_ai.core.repository import iter_source_files


def build_import_graph(root: Path) -> nx.DiGraph:
    graph = nx.DiGraph()
    for path in iter_source_files(root):
        rel = str(path.relative_to(root)); graph.add_node(rel, kind="module")
        if path.suffix == ".py":
            try:
                tree = ast.parse(path.read_text(errors="ignore"))
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names: graph.add_edge(rel, alias.name, kind="imports")
                elif isinstance(node, ast.ImportFrom) and node.module:
                    graph.add_edge(rel, node.module, kind="imports")
    return graph


def impacted_by(graph: nx.DiGraph, module: str) -> list[str]:
    if module not in graph:
        return []
    return sorted(nx.ancestors(graph, module))
