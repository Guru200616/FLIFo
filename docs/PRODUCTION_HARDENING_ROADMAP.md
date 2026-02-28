# LIFO Production Hardening Roadmap (Execution-Ready)

This repository currently does not contain the existing frontend/backend source files, so this document provides a concrete implementation blueprint and starter artifacts to execute your requested migration with minimal ambiguity.

## Phase 1 (Immediate)

### 1) PostgreSQL migration (priority #1)
- Replace SQLite driver with `pg` + pooled connections.
- Add migration scripts from `docs/sql`.
- Configure managed DB via `DATABASE_URL`.
- Introduce startup migration step.

Backend implementation checklist:
1. Install packages:
   - `npm i pg`
   - `npm i -D @types/pg`
2. Replace all direct SQLite calls with `Pool.query` calls.
3. Add a DB module exposing a singleton pool.
4. Ensure indexes exist on tenant-scoped and scheduler-scoped queries.

### 2) Refresh-token rotation
- Persist refresh tokens server-side.
- Store refresh token in `httpOnly`, `secure`, `sameSite=strict` cookie.
- Rotate token at login/refresh.
- Add logout endpoint that revokes the active token.
- Keep a server-side blacklist/revocation mechanism.

### 3) Soft delete strategy
- Add `is_deleted boolean not null default false` to mutable business tables.
- Replace hard deletes with `UPDATE ... SET is_deleted = true`.
- Ensure every read query excludes soft-deleted rows.

### 4) Remove default admin credentials
- Remove hardcoded admin (`admin@lifo.com` / `admin123`).
- Use setup-time seed from environment:
  - `SEED_ADMIN_EMAIL`
  - `SEED_ADMIN_PASSWORD`
- Seed only if no admin exists.

### 5) API versioning
- Prefix all backend endpoints with `/api/v1`.
- Keep an unversioned `/health` endpoint for infra probes.

---

## Phase 2 (Scalability)

### Redis integration
Use Redis for:
- Refresh token/session indexing (optional hybrid with Postgres).
- Cache for dashboard aggregates.
- Distributed lock for scheduler single-execution semantics.

### Scheduler duplication fix
Recommended implementation:
- Redis `SET lock_key value NX EX 60` heartbeat lock.
- Run jobs only while lock is held.
- Release lock safely with value check (Lua script).

### Pagination/filtering
Add shared query parser for:
- `page`, `limit` (bounded)
- `sortBy`, `sortOrder`
- domain filters

---

## Phase 3 (Enterprise)

- Audit logging table for before/after state tracking.
- Sentry for errors/perf.
- Dockerized stack for backend+postgres+redis.

---

## Recommended implementation order
1. Database migration to PostgreSQL
2. Refresh token rotation + logout/revocation
3. Soft delete conversion
4. Redis + scheduler lock
5. Docker + deployment
6. Monitoring
7. Audit logging
