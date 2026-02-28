import crypto from "node:crypto";
import jwt from "jsonwebtoken";
import { env } from "../config/env";
import { pool } from "../db/postgres";

type UserClaims = {
  id: string;
  role: string;
  tenantId: string;
};

const hashToken = (rawToken: string): string => {
  return crypto.createHash("sha256").update(rawToken).digest("hex");
};

export const issueTokens = async (user: UserClaims): Promise<{ accessToken: string; refreshToken: string }> => {
  const accessToken = jwt.sign(
    { sub: user.id, role: user.role, tenantId: user.tenantId },
    env.jwtAccessSecret,
    { expiresIn: env.accessTokenTtl }
  );

  const refreshToken = jwt.sign({ sub: user.id, tenantId: user.tenantId }, env.jwtRefreshSecret, {
    expiresIn: `${env.refreshTokenTtlDays}d`
  });

  const expiresAt = new Date(Date.now() + env.refreshTokenTtlDays * 24 * 60 * 60 * 1000);
  await pool.query(
    `INSERT INTO refresh_tokens (user_id, token_hash, expires_at)
     VALUES ($1, $2, $3)`,
    [user.id, hashToken(refreshToken), expiresAt]
  );

  return { accessToken, refreshToken };
};

export const rotateRefreshToken = async (currentRefreshToken: string): Promise<{ accessToken: string; refreshToken: string }> => {
  const payload = jwt.verify(currentRefreshToken, env.jwtRefreshSecret) as { sub: string; tenantId: string };
  const currentHash = hashToken(currentRefreshToken);

  const currentToken = await pool.query(
    `SELECT * FROM refresh_tokens
     WHERE token_hash = $1 AND revoked_at IS NULL AND is_blacklisted = FALSE AND expires_at > NOW()`,
    [currentHash]
  );

  if (!currentToken.rowCount) {
    throw new Error("Refresh token is invalid or expired");
  }

  const userResult = await pool.query(
    `SELECT id, role, tenant_id AS "tenantId"
     FROM users
     WHERE id = $1 AND is_deleted = FALSE`,
    [payload.sub]
  );

  if (!userResult.rowCount) {
    throw new Error("User no longer active");
  }

  const user = userResult.rows[0] as UserClaims;
  const nextTokens = await issueTokens(user);

  await pool.query(
    `UPDATE refresh_tokens
     SET revoked_at = NOW(), replaced_by_token_hash = $1
     WHERE token_hash = $2`,
    [hashToken(nextTokens.refreshToken), currentHash]
  );

  return nextTokens;
};

export const revokeRefreshToken = async (refreshToken: string): Promise<void> => {
  await pool.query(
    `UPDATE refresh_tokens
     SET revoked_at = NOW(), is_blacklisted = TRUE
     WHERE token_hash = $1`,
    [hashToken(refreshToken)]
  );
};
