# usage.md

## repository inspection

```bash
pyrepofile repo .
pyrepofile repo /path/to/myrepo --format json
pyrepofile repo . --format markdown > report.md
```

The default format is `text`. Unknown repository languages fall back to `Unknown`.

## discovery

```bash
pyrepofile discover .
pyrepofile discover /workspaces --language Python --limit 10
pyrepofile discover /monorepos --pattern "api|service" --format json
```

Scan candidates are directories directly under the chosen root. Dot directories and common dependency
or build directories are skipped.
