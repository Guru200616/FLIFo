from __future__ import annotations

from pathlib import Path
from acia.agents.summary import summarize_repository
from acia.core.repository import detect_frameworks, detect_languages


def generate_documentation(root: Path) -> dict[str, str]:
    summary = summarize_repository(root)
    languages = ", ".join(detect_languages(root)) or "Unknown"
    frameworks = ", ".join(detect_frameworks(root)) or "None detected"
    readme = f"# Repository Documentation\n\n{summary['repository_summary']}\n\nLanguages: {languages}\n\nFrameworks: {frameworks}\n"
    return {
        "readme": readme,
        "setup_guide": "## Setup Guide\n\nInstall dependencies, configure environment variables, and run the FastAPI or frontend dev server for local development.",
        "api_docs": "## API Documentation\n\nDocumented API routes should include purpose, request parameters, response shape, authentication, and error cases.",
        "developer_guide": "## Developer Guide\n\nUse repository summaries, dependency graphs, security scans, and impact analysis before changing core modules.",
    }
