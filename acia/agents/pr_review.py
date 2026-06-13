from __future__ import annotations

from pathlib import Path
from acia.agents.security import scan_repository


def review_changed_files(root: Path, changed_files: list[str]) -> dict[str, object]:
    findings = [f for f in scan_repository(root) if f.file_path in set(changed_files)]
    return {
        "changed_files": changed_files,
        "security_risks": findings,
        "code_smells": ["Validate complexity and coupling for modified modules."],
        "breaking_changes": ["Review public API signatures and persisted schema changes."],
    }
