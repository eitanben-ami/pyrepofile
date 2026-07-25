from __future__ import annotations

import json
from typing import Iterable, List, Union

from pyrepofile.parser import RepoInfo


def render_repo_report(info: RepoInfo, fmt: str = "text") -> str:
    if fmt == "json":
        return json.dumps(
            {
                "path": str(info.path),
                "name": info.name,
                "language": info.language,
                "manifests": info.manifests,
                "manifest_count": info.manifest_count,
            },
            indent=2,
        )

    if fmt == "markdown":
        lines = [f"# {info.name}", "", f"- Path: `{info.path}`", f"- Language: {info.language or 'Unknown'}", f"- manifest_count: {info.manifest_count}", ""]
        if info.manifests:
            lines.extend(["- Manifests:", "".join(f"  - {manifest}" for manifest in info.manifests), ""])
        return "\n".join(lines).rstrip() + "\n"

    lines = [f"repository : {info.name}", f"path       : {info.path}"]
    if info.language:
        lines.append(f"language   : {info.language}")
    lines.extend([f"manifest_count : {info.manifest_count}", "manifests  :"])
    if info.manifests:
        for manifest in info.manifests:
            lines.append(f"  - {manifest}")
    return "\n".join(lines)


def render_report(repos: List[RepoInfo], fmt: str = "text") -> str:
    if fmt == "json":
        payload = [
            {
                "path": str(repo.path),
                "name": repo.name,
                "language": repo.language,
                "manifests": repo.manifests,
                "manifest_count": repo.manifest_count,
            }
            for repo in repos
        ]
        return json.dumps({"repositories": payload, "count": len(payload)}, indent=2)

    if fmt == "markdown":
        sections = [f"# Repository scan", "", f"Found {len(repos)} repository{'ies' if len(repos) != 1 else ''}.", ""]
        for repo in repos:
            sections.append(f"## {repo.name}")
            sections.append("")
            sections.append(f"- Path: `{repo.path}`")
            sections.append(f"- Language: {repo.language or 'Unknown'}")
            sections.append(f"- manifest_count: {repo.manifest_count}")
            if repo.manifests:
                sections.append("- Manifests:")
                for manifest in repo.manifests:
                    sections.append(f"  - {manifest}")
            sections.append("")
        return "\n".join(sections).rstrip() + "\n"

    blocks: List[str] = [f"Found {len(repos)} repository{'ies' if len(repos) != 1 else ''}:"]
    for index, repo in enumerate(repos, start=1):
        lines = [f"[{index}] {repo.name}", f"     path       : {repo.path}"]
        if repo.language:
            lines.append(f"     language   : {repo.language}")
        lines.extend([f"     manifest_count : {repo.manifest_count}", "     manifests  :"])
        if repo.manifests:
            for manifest in repo.manifests:
                lines.append(f"       - {manifest}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)
