# CodeSage AI – Autonomous Code Intelligence Agent

CodeSage AI is a production-grade multi-agent AI developer platform blueprint and MVP for repository-wide GitHub intelligence. It clones and indexes repositories, extracts code symbols, builds retrieval context, detects security risks, creates dependency graphs, and exposes natural-language repository Q&A APIs.

**Tagline:** Understand, Explain, Secure, Review, and Analyze Any GitHub Repository with AI

## Branding and Identity

- **Short product name:** CodeSage AI
- **Full product name:** CodeSage AI – Autonomous Code Intelligence Agent
- **Repository name:** `codesage-ai`
- **Visual identity:** modern enterprise AI engineering platform with deep indigo foundations, electric cyan intelligence accents, and accessible slate neutrals.
  - Primary: `#312E81` (enterprise indigo)
  - Secondary: `#06B6D4` (AI cyan)
  - Accent: `#A855F7` (agentic violet)
  - Surface: `#0F172A` (developer slate)
  - Success: `#10B981` (secure green)

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
uvicorn codesage_ai.main:app --reload
```

## Example Endpoints

- `GET /health`
- `POST /api/v1/repositories/validate`
- `GET /api/v1/analyze/local?path=.`
- `GET /api/v1/chat/local?path=.&question=How does login work?`
- `GET /api/v1/security/local?path=.`
- `GET /api/v1/impact/local?path=.&module=service.py`

## SEO and Social Metadata

- **Browser title:** CodeSage AI – Autonomous Code Intelligence Agent
- **Meta description:** Understand, Explain, Secure, Review, and Analyze Any GitHub Repository with AI.
- **Open Graph title:** CodeSage AI – Autonomous Code Intelligence Agent
- **Open Graph description:** Enterprise-ready AI repository intelligence for code understanding, security review, impact analysis, and documentation.
- **Open Graph site name:** CodeSage AI

## UI Copy Guidance

Use **CodeSage AI** for navbar branding, footer branding, loading screens, dashboard titles, error pages, empty states, and other short user-facing labels. Use **CodeSage AI – Autonomous Code Intelligence Agent** for landing-page heroes, browser tab titles, API documentation titles, deployment marketplace listings, and other full-title contexts.

See `docs/CODESAGE_AI_ARCHITECTURE.md` for the full architecture and roadmap.
