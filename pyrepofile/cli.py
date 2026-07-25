from pathlib import Path

from pyrepofile.parser import parse_repository, list_repositories
from pyrepofile.reporter import render_report, render_repo_report


def _cmd_repo(args):
    path = Path(args.path).resolve()
    info = parse_repository(path)
    print(render_repo_report(info, fmt=args.format))


def _cmd_discover(args):
    root = Path(args.root).resolve()
    limit = args.limit
    fmt = args.format
    language = args.language
    pattern = args.pattern
    repos = list_repositories(root, language=language, pattern=pattern, limit=limit)
    print(render_report(repos, fmt=fmt))


def main(argv=None) -> int:
    import argparse
    parser = argparse.ArgumentParser(prog="pyrepofile", description="Scan local directories and summarize repositories by their manifest files.")
    sub = parser.add_subparsers(dest="command")

    repo = sub.add_parser("repo", help="Show manifest files for one repository")
    repo.add_argument("path", help="Path to repository root")
    repo.add_argument("--format", choices=["text", "json", "markdown"], default="text")

    discover = sub.add_parser("discover", help="Discover repositories under a root directory")
    discover.add_argument("root", nargs="?", default=".", help="Root directory to scan")
    discover.add_argument("--language", help="Filter by language", default=None)
    discover.add_argument("--pattern", help="Regex filter for repository path/name", default=None)
    discover.add_argument("--limit", type=int, default=50)
    discover.add_argument("--format", choices=["text", "json", "markdown"], default="text")

    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 1
    if args.command == "repo":
        _cmd_repo(args)
    elif args.command == "discover":
        _cmd_discover(args)
    return 0
