from __future__ import annotations

from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from acia.agents.orchestrator import RepositoryIntelligenceOrchestrator
from acia.core.repository import validate_github_url
from acia.models.schemas import RepositoryIngestRequest
from acia.agents.documentation import generate_documentation
from acia.agents.flow import trace_execution_flow
from acia.agents.pr_review import review_changed_files
from acia.agents.summary import summarize_repository
from acia.agents.test_generation import generate_tests

app = FastAPI(title="ACIA Repository Intelligence API", version="0.1.0")
orchestrator = RepositoryIntelligenceOrchestrator()


@app.get("/health")
def health() -> dict[str, bool | str]:
    return {"ok": True, "service": "acia"}


@app.post("/api/v1/repositories/validate")
def validate_repository(request: RepositoryIngestRequest) -> dict[str, str]:
    try:
        return {"url": validate_github_url(str(request.url)), "status": "accepted"}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/v1/analyze/local")
def analyze_local(path: str = Query(".", description="Local repository path mounted for analysis")):
    root = Path(path).resolve()
    if not root.exists() or not root.is_dir():
        raise HTTPException(status_code=404, detail="Repository path not found")
    return orchestrator.analyze(root)


@app.get("/api/v1/chat/local")
def chat_local(question: str, path: str = "."):
    root = Path(path).resolve()
    if not root.exists() or not root.is_dir():
        raise HTTPException(status_code=404, detail="Repository path not found")
    return orchestrator.answer(root, question)


@app.get("/api/v1/security/local")
def security_local(path: str = "."):
    root = Path(path).resolve()
    if not root.exists() or not root.is_dir():
        raise HTTPException(status_code=404, detail="Repository path not found")
    return orchestrator.security(root)


@app.get("/api/v1/impact/local")
def impact_local(module: str, path: str = "."):
    root = Path(path).resolve()
    if not root.exists() or not root.is_dir():
        raise HTTPException(status_code=404, detail="Repository path not found")
    return orchestrator.impact(root, module)



@app.get("/api/v1/summary/local")
def summary_local(path: str = "."):
    root = Path(path).resolve()
    if not root.exists() or not root.is_dir():
        raise HTTPException(status_code=404, detail="Repository path not found")
    return summarize_repository(root)


@app.get("/api/v1/flows/local")
def flows_local(flow: str, path: str = "."):
    root = Path(path).resolve()
    if not root.exists() or not root.is_dir():
        raise HTTPException(status_code=404, detail="Repository path not found")
    return trace_execution_flow(root, flow)


@app.get("/api/v1/documentation/local")
def documentation_local(path: str = "."):
    root = Path(path).resolve()
    if not root.exists() or not root.is_dir():
        raise HTTPException(status_code=404, detail="Repository path not found")
    return generate_documentation(root)


@app.get("/api/v1/tests/local")
def tests_local(path: str = ".", framework: str = "pytest"):
    root = Path(path).resolve()
    if not root.exists() or not root.is_dir():
        raise HTTPException(status_code=404, detail="Repository path not found")
    return generate_tests(root, framework)


@app.post("/api/v1/pr-review/local")
def pr_review_local(changed_files: list[str], path: str = "."):
    root = Path(path).resolve()
    if not root.exists() or not root.is_dir():
        raise HTTPException(status_code=404, detail="Repository path not found")
    return review_changed_files(root, changed_files)
