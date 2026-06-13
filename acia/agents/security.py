from __future__ import annotations

import re
from pathlib import Path
from acia.core.repository import iter_source_files
from acia.models.schemas import SecurityFinding, Severity

RULES = [
    ("Hardcoded secret", Severity.high, re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}"), "Move secrets to encrypted secret storage and rotate exposed values."),
    ("Possible SQL injection", Severity.critical, re.compile(r"execute\([^\n]*(\+|f['\"])"), "Use parameterized queries or ORM bind parameters."),
    ("Command injection risk", Severity.critical, re.compile(r"(subprocess|exec|system|spawn)\([^\n]*(shell\s*=\s*True|\+)"), "Avoid shell execution and pass arguments as an array after validation."),
    ("Weak JWT configuration", Severity.high, re.compile(r"(?i)jwt\.(encode|sign)\([^\n]*(none|HS256|expiresIn\s*:\s*['\"]?\d+[yY])"), "Use strong algorithms, short expiration, rotation, and server-side revocation."),
]


def scan_repository(root: Path) -> list[SecurityFinding]:
    findings: list[SecurityFinding] = []
    for path in iter_source_files(root):
        rel = str(path.relative_to(root))
        for idx, line in enumerate(path.read_text(errors="ignore").splitlines(), start=1):
            for issue, severity, pattern, rec in RULES:
                if pattern.search(line):
                    findings.append(SecurityFinding(issue=issue, severity=severity, file_path=rel, line=idx, evidence=line.strip()[:180], recommendation=rec))
    return findings
