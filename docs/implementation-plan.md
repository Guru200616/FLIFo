# LIFO Production Hardening Plan

## Phase 1 (Immediate)

1. **PostgreSQL migration**
   - Install: `npm i pg`
   - Replace SQLite client with `pg.Pool` using `DATABASE_URL`.
   - Apply `sql/001_initial_postgres.sql`.
   - Smoke test all write paths under concurrent load.

2. **Refresh token rotation**
   - Store refresh token in httpOnly, secure cookie.
   - Persist only token hash in `refresh_tokens`.
   - Rotate on every `/api/v1/auth/refresh`.
   - Revoke current token row on logout.
   - Blacklist access-token `jti` on forced logout.

3. **Soft delete**
   - Add `is_deleted` boolean to domain tables.
   - Replace `DELETE` queries with `UPDATE ... SET is_deleted = TRUE`.
   - Add default filters (`is_deleted = FALSE`) in reads.

4. **Remove default admin credentials**
   - Use setup-time variables:
     - `BOOTSTRAP_ADMIN_EMAIL`
     - `BOOTSTRAP_ADMIN_PASSWORD`
   - Seed once, then disable seed mode.

5. **API versioning**
   - Prefix all routes with `/api/v1`.
   - Example:
     - `/api/v1/auth/login`
     - `/api/v1/users?page=1&limit=20`

## Phase 2

6. Redis for caching + token/session helpers + scheduler lock.
7. Scheduler deduplication with Redis lock or BullMQ worker.
8. Pagination/filtering/sorting on supervisor dashboards.

## Phase 3

9. Audit logging on all privileged mutations.
10. Sentry error + performance monitoring and `/healthz` endpoint.
11. Dockerized deployment.
12. Managed deployment split:
    - Frontend: Vercel
    - Backend: Render/Railway
    - DB: managed Postgres
    - Cache: managed Redis
