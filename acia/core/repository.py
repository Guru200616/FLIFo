from __future__ import annotations

import re
from pathlib import Path

IGNORE_DIRS = {".git", "node_modules", "build", "dist", "vendor", "__pycache__", ".venv"}
EXTENSION_LANGUAGE = {
    ".py": "Python", ".js": "JavaScript", ".jsx": "JavaScript", ".ts": "TypeScript",
    ".tsx": "TypeScript", ".go": "Go", ".java": "Java", ".cs": "C#", ".cpp": "C++",
    ".cc": "C++", ".cxx": "C++", ".rs": "Rust",
}


def validate_github_url(url: str) -> str:
    """Allow only canonical GitHub repository URLs to prevent shell/path injection."""
    pattern = r"^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?/?$"
    if not re.match(pattern, url):
        raise ValueError("Only canonical https://github.com/<owner>/<repo> URLs are supported")
    return url.rstrip("/")


def iter_source_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.suffix in EXTENSION_LANGUAGE:
            yield path


def detect_languages(root: Path) -> list[str]:
    langs = {EXTENSION_LANGUAGE[p.suffix] for p in iter_source_files(root)}
    return sorted(langs)


def detect_frameworks(root: Path) -> list[str]:
    frameworks: set[str] = set()
    manifests = {p.name: p for p in root.glob("*") if p.is_file()}
    package_json = manifests.get("package.json")
    if package_json:
        text = package_json.read_text(errors="ignore")
        for name in ("react", "next", "express", "nestjs", "vite"):
            if f'"{name}"' in text:
                frameworks.add(name)
    if (root / "pyproject.toml").exists() or (root / "requirements.txt").exists():
        text = "\n".join(p.read_text(errors="ignore") for p in [root / "pyproject.toml", root / "requirements.txt"] if p.exists())
        for name in ("fastapi", "django", "flask", "langgraph"):
            if name in text.lower():
                frameworks.add(name)
    return sorted(frameworks)
