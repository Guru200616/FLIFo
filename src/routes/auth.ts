import bcrypt from "bcryptjs";
import { Request, Response, Router } from "express";
import { env } from "../config/env";
import { pool } from "../db/postgres";
import { issueTokens, revokeRefreshToken, rotateRefreshToken } from "../services/tokenService";

export const authRouter = Router();

const refreshCookieConfig = {
  httpOnly: true,
  secure: env.nodeEnv === "production",
  sameSite: "strict" as const,
  path: "/api/v1/auth"
};

authRouter.post("/login", async (req: Request, res: Response) => {
  const { email, password } = req.body as { email: string; password: string };

  const userResult = await pool.query(
    `SELECT id, role, tenant_id AS "tenantId", password_hash AS "passwordHash"
     FROM users
     WHERE email = $1 AND is_deleted = FALSE`,
    [email]
  );

  if (!userResult.rowCount) {
    res.status(401).json({ message: "Invalid credentials" });
    return;
  }

  const user = userResult.rows[0] as { id: string; role: string; tenantId: string; passwordHash: string };
  const validPassword = await bcrypt.compare(password, user.passwordHash);
  if (!validPassword) {
    res.status(401).json({ message: "Invalid credentials" });
    return;
  }

  const tokens = await issueTokens({ id: user.id, role: user.role, tenantId: user.tenantId });
  res.cookie(env.refreshCookieName, tokens.refreshToken, refreshCookieConfig);
  res.json({ accessToken: tokens.accessToken });
});

authRouter.post("/refresh", async (req: Request, res: Response) => {
  const refreshToken = req.cookies[env.refreshCookieName] as string | undefined;
  if (!refreshToken) {
    res.status(401).json({ message: "Missing refresh cookie" });
    return;
  }

  try {
    const tokens = await rotateRefreshToken(refreshToken);
    res.cookie(env.refreshCookieName, tokens.refreshToken, refreshCookieConfig);
    res.json({ accessToken: tokens.accessToken });
  } catch {
    res.status(401).json({ message: "Invalid refresh token" });
  }
});

authRouter.post("/logout", async (req: Request, res: Response) => {
  const refreshToken = req.cookies[env.refreshCookieName] as string | undefined;
  if (refreshToken) {
    await revokeRefreshToken(refreshToken);
  }
  res.clearCookie(env.refreshCookieName, refreshCookieConfig);
  res.status(204).send();
});
