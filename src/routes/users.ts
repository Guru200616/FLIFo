import { Response, Router } from "express";
import { pool } from "../db/postgres";
import { AuthenticatedRequest, requireAuth, requireRole } from "../middleware/auth";

export const usersRouter = Router();

usersRouter.use(requireAuth);

usersRouter.get("/", requireRole("admin", "supervisor"), async (req: AuthenticatedRequest, res: Response) => {
  const page = Math.max(Number(req.query.page ?? 1), 1);
  const limit = Math.min(Math.max(Number(req.query.limit ?? 20), 1), 100);
  const offset = (page - 1) * limit;
  const role = (req.query.role as string | undefined) ?? null;
  const sortDirection = String(req.query.sort ?? "asc").toLowerCase() === "desc" ? "DESC" : "ASC";

  const params: unknown[] = [req.user?.tenantId, limit, offset];
  const roleFilter = role ? `AND role = $4` : "";
  if (role) params.push(role);

  const result = await pool.query(
    `SELECT id, email, role, created_at
     FROM users
     WHERE tenant_id = $1 AND is_deleted = FALSE ${roleFilter}
     ORDER BY created_at ${sortDirection}
     LIMIT $2 OFFSET $3`,
    params
  );

  res.json({ page, limit, data: result.rows });
});

usersRouter.delete("/:id", requireRole("admin"), async (req: AuthenticatedRequest, res: Response) => {
  const { id } = req.params;
  const result = await pool.query(
    `UPDATE users
     SET is_deleted = TRUE, updated_at = NOW()
     WHERE id = $1 AND tenant_id = $2 AND is_deleted = FALSE`,
    [id, req.user?.tenantId]
  );

  if (!result.rowCount) {
    res.status(404).json({ message: "User not found" });
    return;
  }

  await pool.query(
    `INSERT INTO audit_logs (user_id, action_type, entity_name, after_state)
     VALUES ($1, 'soft_delete', 'users', $2::jsonb)`,
    [req.user?.sub, JSON.stringify({ id, is_deleted: true })]
  );

  res.status(204).send();
});
