# LIFO Production Hardening Blueprint

This repository currently does not contain the application source files required to directly patch the existing React/Express implementation.

To keep delivery moving, this document captures the production-grade implementation plan and concrete artifacts that can be applied once the backend/frontend source tree is present.

## Phase 1 (Immediate): Production Hardening

### 1) PostgreSQL migration (from SQLite)

- Add dependency:
  - `npm install pg`
- Replace SQLite client with a `pg.Pool` configured via env vars.
- Add migration runner (or use your ORM migration system).
- Use managed Postgres (Neon/Supabase/Railway) for production.

Suggested env vars:

- `DATABASE_URL`
- `PGSSLMODE=require`

### 2) Refresh token rotation

- Add `refresh_tokens` table (see `migrations/001_init_postgres.sql`).
- Store only a hashed refresh token in DB.
- Set refresh token in secure `httpOnly` cookie.
- Rotate on login and on refresh endpoint.
- Revoke on logout (delete or mark revoked).

Recommended endpoints:

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`

### 3) Soft deletes

- Add `is_deleted BOOLEAN NOT NULL DEFAULT FALSE` to mutable entities.
- Replace hard delete with update:
  - `UPDATE <table> SET is_deleted = TRUE, updated_at = NOW() WHERE id = $1;`
- Add `WHERE is_deleted = FALSE` to all read queries.

### 4) Remove default admin credentials

- Remove hardcoded credentials entirely.
- Seed admin through environment variables (`ADMIN_EMAIL`, `ADMIN_PASSWORD`) at setup time only.
- Force password change on first login.

### 5) API versioning

- Prefix all routes with `/api/v1`.
- Keep v1 contract stable and isolate breaking changes into `/api/v2` later.

## Phase 2: Scalability & performance

- Add Redis (`npm install redis`) for:
  - dashboard caching
  - refresh token/session lookup
  - distributed lock for scheduler
- Avoid duplicate schedulers in multi-instance deployments:
  - implement Redis lock with TTL, or
  - move to separate worker (BullMQ strongly recommended)
- Add pagination/filtering to list APIs:
  - `GET /api/v1/users?page=1&limit=20&sort=created_at:desc`

## Phase 3: Enterprise controls

- Audit logs (`audit_logs` table in migration).
- Monitoring with Sentry (`@sentry/node`) + health endpoint (`/healthz`).
- Containerize app and deploy frontend/backend/db/redis on managed providers.

## Suggested implementation order

1. PostgreSQL cutover + migration validation
2. Refresh-token rotation + logout/revocation
3. Soft delete pass on all entities
4. Redis + scheduler lock
5. Docker/deployment templates
6. Monitoring
7. Audit logging exposure/reporting
