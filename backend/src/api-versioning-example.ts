import { Router } from 'express';

const v1 = Router();

v1.get('/health', (_req, res) => {
  res.json({ ok: true, version: 'v1' });
});

export const apiRouter = Router().use('/api/v1', v1);
