from pathlib import Path

import pytest

from pyrepofile.parser import RepoInfo, parse_repository, repo_language
from pyrepofile.reporter import render_report, render_repo_report


def test_repo_language_detection():
    assert repo_language([]) is None
    assert repo_language(["unknown_file.bin", "README.md"]) is None
    assert repo_language(["pyproject.toml"]) == "Python"
    assert repo_language(["package.json"]) == "Node"
    assert repo_language(["go.mod"]) == "Go"
    assert repo_language(["Cargo.toml"]) == "Rust"


def test_parse_repository(tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("[project]\n")
    pkg = tmp_path / "pkg" / "core.py"
    pkg.parent.mkdir()
    pkg.write_text("print('hi')\n")

    info = parse_repository(tmp_path)
    assert info.language == "Python"
    assert info.name == tmp_path.name
    assert "pyproject.toml" in info.manifests
    assert info.manifest_count >= 1


def test_parse_repository_missing_path():
    with pytest.raises(FileNotFoundError):
        parse_repository(Path("/tmp/__pyrepofile_missing_dir_91023"))


def test_render_repo_report_text():
    info = RepoInfo(path=Path("/tmp/sample"), language="Python", manifests=["pyproject.toml", "README.md"])
    text = render_repo_report(info, fmt="text")
    assert "/tmp/sample" in text
    assert "manifest_count" in text
    assert "pyproject.toml" in text


def test_render_repo_report_json():
    info = RepoInfo(path=Path("/tmp/sample"), language="Python", manifests=["pyproject.toml", "README.md"])
    json_output = render_repo_report(info, fmt="json")
    assert "pyproject.toml" in json_output
    assert "/tmp/sample" in json_output


def test_render_repo_report_markdown():
    info = RepoInfo(path=Path("/tmp/sample"), language="Python", manifests=["pyproject.toml", "README.md"])
    md = render_repo_report(info, fmt="markdown")
    assert "# sample" in md
    assert "pyproject.toml" in md
    assert "- Path:" in md


def test_discover_repositories_limit(tmp_path):
    repo_a = tmp_path / "alpha"
    repo_b = tmp_path / "beta"
    repo_c = tmp_path / "charlie"
    for repo in [repo_a, repo_b, repo_c]:
        repo.mkdir()
        (repo / "README.md").write_text("# repo\n")

    (repo_a / "pyproject.toml").write_text("[project]\n")
    (repo_b / "package.json").write_text("{\"name\":\"beta\"}\n")

    from pyrepofile.parser import list_repositories
    results = list_repositories(tmp_path, limit=2)

    assert len(results) == 2
    languages = {info.language for info in results}
    assert len(languages) == 2
    paths = {info.path.name for info in results}
    assert paths.issubset({"alpha", "beta", "charlie"})
