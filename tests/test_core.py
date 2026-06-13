from pathlib import Path
import pytest
from acia.core.repository import validate_github_url, detect_languages
from acia.core.parser import parse_repository
from acia.agents.retrieval import bm25_search


def test_validate_github_url_accepts_canonical():
    assert validate_github_url("https://github.com/openai/example.git") == "https://github.com/openai/example.git"


def test_validate_github_url_rejects_injection():
    with pytest.raises(ValueError):
        validate_github_url("https://github.com/openai/example.git;rm -rf /")


def test_parse_and_retrieve_python(tmp_path: Path):
    source = tmp_path / "service.py"
    source.write_text("def login_user(name):\n    return {'token': name}\n")
    symbols, chunks = parse_repository(tmp_path)
    assert symbols[0].name == "login_user"
    assert detect_languages(tmp_path) == ["Python"]
    assert bm25_search("where is login token", chunks)[0].symbol == "login_user"
