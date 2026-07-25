from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)
class RepoInfo:
    path: Path
    language: Optional[str]
    manifests: list[str] = field(default_factory=list)
    name: str = ""

    def __post_init__(self) -> None:
        if not self.name:
            object.__setattr__(self, "name", self.path.name or str(self.path))

    @property
    def manifest_count(self) -> int:
        return len(self.manifests)


LANGUAGE_FILES: dict[str, list[str]] = {
    "Python": ["pyproject.toml", "setup.py", "requirements.txt", "setup.cfg", "Pipfile"],
    "Node": ["package.json"],
    "Go": ["go.mod", "go.sum"],
    "Rust": ["Cargo.toml", "Cargo.lock"],
    "Ruby": ["Gemfile"],
    "Java": ["pom.xml", "build.gradle"],
    "CSharp": [".csproj", ".sln"],
    "PHP": ["composer.json"],
}


def repo_language(manifests: Iterable[str]) -> Optional[str]:
    available = set(manifests)
    for language, files in LANGUAGE_FILES.items():
        if any(f in available for f in files):
            return language
    return None


def parse_repository(path: Path) -> RepoInfo:
    if not path.is_dir():
        raise FileNotFoundError(f"Repository path does not exist: {path}")

    manifests = sorted({entry.name for entry in path.iterdir() if entry.is_file() and not entry.name.startswith(".")})
    language = repo_language(manifests)
    return RepoInfo(path=path, language=language, manifests=manifests)


def list_repositories(
    root: Path,
    *,
    language: Optional[str] = None,
    pattern: Optional[str] = None,
    limit: int = 50,
) -> list[RepoInfo]:
    if not root.is_dir():
        raise FileNotFoundError(f"Root path does not exist: {root}")

    compiled = re.compile(pattern) if pattern else None
    found: list[RepoInfo] = []

    for entry in sorted(root.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith("."):
            continue
        if entry.name in {"__pycache__", ".venv", "node_modules", "dist", "build", ".git", ".idea"}:
            continue
        if compiled and not compiled.search(entry.name) and not compiled.search(str(entry)):
            continue

        info = parse_repository(entry)
        if language and info.language != language:
            continue
        found.append(info)
        if len(found) >= limit:
            break

    found.sort(key=lambda item: (item.language or "zzz", item.name.lower()))
    return found
