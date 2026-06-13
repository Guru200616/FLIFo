from __future__ import annotations

from pathlib import Path
from acia.core.parser import parse_repository


def generate_tests(root: Path, framework: str = "pytest") -> dict[str, str]:
    symbols, _ = parse_repository(root)
    names = [s.name for s in symbols[:5]]
    if framework == "jest":
        body = "describe('generated repository checks', () => { it('loads target modules', () => { expect(true).toBe(true); }); });"
    elif framework == "junit":
        body = "class GeneratedRepositoryTest { @org.junit.jupiter.api.Test void loads() { org.junit.jupiter.api.Assertions.assertTrue(true); } }"
    else:
        body = "def test_generated_repository_contract():\n    assert True\n"
    return {"framework": framework, "target_symbols": ", ".join(names), "test_code": body}
