from __future__ import annotations

from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from acia.agents.orchestrator import RepositoryIntelligenceOrchestrator
from acia.core.repository import validate_github_url
from acia.models.schemas import RepositoryIngestRequest

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
