# CodeSage AI – Autonomous Code Intelligence Agent

CodeSage AI is a production-oriented multi-agent platform for GitHub repository intelligence. It is designed to behave like a senior engineer that has already studied a repository and can answer questions, review changes, trace flows, detect vulnerabilities, generate documentation, and predict change impact.

**Tagline:** Understand, Explain, Secure, Review, and Analyze Any GitHub Repository with AI

## Platform Layers

1. **FastAPI API layer** exposes repository validation, local analysis, chat, security, and impact endpoints under `/api/v1`, while keeping `/health` unversioned for infrastructure probes.
2. **Repository core** validates GitHub URLs, scans supported source files, ignores generated/vendor directories, and detects languages/frameworks.
3. **Parsing and indexing** extracts symbols and function/class chunks. The MVP uses Python AST and language-aware textual extraction; production can swap in Tree-sitter without changing agent contracts.
4. **Agent facade** coordinates repository overview, retrieval, security, graph, and impact analysis. This facade is intentionally shaped for migration to LangGraph nodes.
5. **Graph intelligence** builds import graphs with NetworkX and provides first-order impact analysis.
6. **Security intelligence** applies deterministic rules for hardcoded secrets, SQL injection, command injection, and weak JWT patterns before optional LLM validation.
7. **Retrieval intelligence** provides BM25 lexical retrieval today and is ready for vector search, BGE embeddings, ChromaDB/Qdrant, and cross-encoder reranking.

## Branding System

- **Product name:** CodeSage AI
- **Full title:** CodeSage AI – Autonomous Code Intelligence Agent
- **Repository:** `codesage-ai`
- **Primary color:** `#312E81`
- **Secondary color:** `#06B6D4`
- **Accent color:** `#A855F7`
- **Developer surface:** `#0F172A`
- **Secure success state:** `#10B981`

This identity should be used consistently in landing pages, navbar branding, footer branding, dashboard headings, browser tab titles, SEO metadata, Open Graph metadata, loading screens, empty states, API documentation, deployment configuration, Docker labels, and generated documentation.

## Production Roadmap Alignment

- **Phase 1:** repository scanning, AST/text parsing, function/class chunking, local chat, API scaffolding.
- **Phase 2:** LangGraph orchestration, hybrid retrieval, dependency graph visualization.
- **Phase 3:** expanded security and review agents with dependency audit integrations.
- **Phase 4:** documentation generation, test generation, PR review, and deeper impact analysis.
- **Phase 5:** knowledge graph persistence, incremental reindexing, GitHub webhooks, OpenTelemetry tracing.

## Security Model

Repository ingestion must validate GitHub URLs before cloning and should clone with argument arrays rather than shell strings. The API currently rejects non-canonical GitHub URLs and avoids arbitrary clone execution in the MVP. Production deployments should add JWT authentication, rate limiting, repository isolation, encrypted secrets, and audit logging.
