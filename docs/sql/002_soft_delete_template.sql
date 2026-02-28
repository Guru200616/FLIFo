-- Template migration for existing business tables.
-- Duplicate/adapt block per table.

-- Example table: patients
ALTER TABLE patients
  ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN NOT NULL DEFAULT FALSE;

CREATE INDEX IF NOT EXISTS idx_patients_active
ON patients(tenant_id, id)
WHERE is_deleted = FALSE;

-- Replace hard-delete queries in app code:
-- DELETE FROM patients WHERE id = $1 AND tenant_id = $2;
-- with:
-- UPDATE patients SET is_deleted = TRUE, updated_at = now() WHERE id = $1 AND tenant_id = $2;
