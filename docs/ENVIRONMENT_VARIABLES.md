# Required Environment Variables for Production

## Backend
- `NODE_ENV=production`
- `PORT=3000`
- `DATABASE_URL=postgresql://...`
- `JWT_ACCESS_SECRET=...`
- `JWT_REFRESH_SECRET=...`
- `ACCESS_TOKEN_TTL=15m`
- `REFRESH_TOKEN_TTL_DAYS=30`
- `COOKIE_DOMAIN=yourdomain.com`
- `CORS_ORIGIN=https://app.yourdomain.com`
- `REDIS_URL=redis://...`
- `SEED_ADMIN_EMAIL=...`
- `SEED_ADMIN_PASSWORD=...`
- `SENTRY_DSN=...`

## Frontend
- `VITE_API_BASE_URL=https://api.yourdomain.com/api/v1`
