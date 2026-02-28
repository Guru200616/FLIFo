import bcrypt from "bcryptjs";
import { env } from "../config/env";
import { pool, runMigrations } from "./postgres";

const seedAdmin = async (): Promise<void> => {
  if (!env.adminEmail || !env.adminPassword) {
    console.info("Skipping admin seed. Set ADMIN_EMAIL and ADMIN_PASSWORD to seed an initial admin.");
    return;
  }

  const existing = await pool.query("SELECT id FROM users WHERE email = $1", [env.adminEmail]);
  if (existing.rowCount) {
    console.info("Admin already exists, skipping seed.");
    return;
  }

  const hash = await bcrypt.hash(env.adminPassword, 12);
  await pool.query(
    `INSERT INTO users (email, password_hash, role)
     VALUES ($1, $2, 'admin')`,
    [env.adminEmail, hash]
  );
  console.info("Seeded initial admin from environment variables.");
};

const main = async (): Promise<void> => {
  try {
    await runMigrations();
    await seedAdmin();
  } finally {
    await pool.end();
  }
};

void main();
