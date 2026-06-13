# ACIA — Autonomous Code Intelligence Agent

ACIA is a production-grade multi-agent AI platform blueprint and MVP for repository-wide GitHub intelligence. It clones and indexes repositories, extracts code symbols, builds retrieval context, detects security risks, creates dependency graphs, and exposes natural-language repository Q&A APIs.

## Current MVP

- FastAPI service with versioned `/api/v1` endpoints and unversioned `/health`.
- GitHub repository URL validation designed to prevent shell injection.
- Source scanning for Python, JavaScript, TypeScript, Go, Java, C#, C++, and Rust.
- Function/class chunking with Python AST and language-aware textual extraction.
- BM25 retrieval for repository chat context.
- NetworkX import graph and first-order impact analysis.
- Rule-based security agent for common high-risk patterns.

## Run

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
uvicorn acia.main:app --reload
```

## Example Endpoints

- `GET /health`
- `POST /api/v1/repositories/validate`
- `GET /api/v1/analyze/local?path=.`
- `GET /api/v1/chat/local?path=.&question=How does login work?`
- `GET /api/v1/security/local?path=.`
- `GET /api/v1/impact/local?path=.&module=service.py`

See `docs/ACIA_ARCHITECTURE.md` for the full architecture and roadmap.
