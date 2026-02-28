# LIFO Production Upgrade Starter

This repository currently contains no application source code, so this starter focuses on production-grade infrastructure and data-model artifacts that can be dropped into the existing LIFO app once the codebase is restored.

## What is included

1. **PostgreSQL migration baseline** (`sql/001_initial_postgres.sql`)
   - Core `users` table with `is_deleted` soft-delete flag.
   - `refresh_tokens` table for rotation + revocation.
   - `token_blacklist` table for access token invalidation.
   - `audit_logs` table for enterprise tracking.

2. **Dockerized local production-like stack** (`docker-compose.yml`)
   - `postgres` service
   - `redis` service
   - `backend` service placeholder

3. **Backend container recipe** (`Dockerfile`)
   - Uses `node:18`
   - Installs dependencies and starts app with `npm run start`

4. **Environment contract** (`.env.example`)
   - JWT and refresh token secrets
   - Postgres and Redis configuration
   - First-admin bootstrap variables (no hardcoded default credentials)

5. **Implementation runbook** (`docs/implementation-plan.md`)
   - Ordered checklist mapped to the exact priority you provided.
   - Endpoint versioning examples under `/api/v1/...`.
   - Refresh token rotation flow and scheduler lock strategy.

## Immediate integration sequence

1. Wire your Express DB layer to `DATABASE_URL` using `pg.Pool`.
2. Apply `sql/001_initial_postgres.sql` on managed PostgreSQL.
3. Implement auth routes:
   - `POST /api/v1/auth/login`
   - `POST /api/v1/auth/refresh`
   - `POST /api/v1/auth/logout`
4. Update all destructive handlers to soft-delete (`is_deleted = TRUE`).
5. Add Redis-backed distributed lock for scheduler before running multi-instance backend.

