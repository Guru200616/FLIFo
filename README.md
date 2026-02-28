# LIFO Production Hardening Baseline

This repository now contains a production-focused backend baseline implementing the highest-priority roadmap items:

- PostgreSQL (`pg`) connection pool and migration bootstrap.
- Refresh token rotation with revocation/blacklisting table.
- Soft-delete strategy (`is_deleted`) on users.
- Removal of default admin credentials in favor of env-seeded setup.
- API versioning under `/api/v1/*`.
- Redis distributed scheduler lock.
- Health check + optional Sentry initialization.
- Docker + docker-compose for backend, Postgres, and Redis.

## Quick start

1. Copy environment file:
   ```bash
   cp .env.example .env
   ```
2. Fill secure values in `.env`.
3. Start local dependencies:
   ```bash
   docker compose up -d postgres redis
   ```
4. Install dependencies and initialize DB:
   ```bash
   npm install
   npm run db:init
   npm run dev
   ```

## Managed services

For production:

- PostgreSQL: Neon/Supabase/Railway managed instance.
- Redis: managed Redis (Upstash/Redis Cloud).
- Backend: Render or Railway.
- Frontend: Vercel.
