import { NextFunction, Request, Response } from "express";
import jwt from "jsonwebtoken";
import { env } from "../config/env";

type AccessPayload = {
  sub: string;
  role: string;
  tenantId: string;
};

export type AuthenticatedRequest = Request & { user?: AccessPayload };

export const requireAuth = (req: AuthenticatedRequest, res: Response, next: NextFunction): void => {
  const authHeader = req.header("authorization");
  if (!authHeader?.startsWith("Bearer ")) {
    res.status(401).json({ message: "Unauthorized" });
    return;
  }

  const token = authHeader.slice(7);
  try {
    const payload = jwt.verify(token, env.jwtAccessSecret) as AccessPayload;
    req.user = payload;
    next();
  } catch {
    res.status(401).json({ message: "Invalid access token" });
  }
};

export const requireRole = (...roles: string[]) => {
  return (req: AuthenticatedRequest, res: Response, next: NextFunction): void => {
    if (!req.user || !roles.includes(req.user.role)) {
      res.status(403).json({ message: "Forbidden" });
      return;
    }
    next();
  };
};
