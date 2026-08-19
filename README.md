# pyrepofile

Scan local directories and summarize projects by their manifest files.

<p align="left">
  <img src="https://img.shields.io/badge/python-3.9%2B-blue" alt="Python" />
  <img src="https://img.shields.io/badge/status-stable-green" alt="Status" />
  <img src="https://img.shields.io/badge/cli-repo%20scan-green" alt="CLI" />
</p>

## About

Project directories often contain recognizable stack markers such as `pyproject.toml`, `package.json`, or `Cargo.toml`.
`pyrepofile` walks candidate project folders and reports which manifest files it finds, the most likely language,
and counts for scripting, review, or CI triage.

## Features

- Inspect a single repository path and list its manifest files.
- Discover repositories under a root directory.
- Classify language by recognized manifest files.
- Text, JSON, and Markdown output formats.
- Editable install.

## Installation

```bash
python -m pip install -e .
```

## Usage

```bash
pyrepofile repo /path/to/repo --format text
pyrepofile discover /path/to/workspace --limit 20 --format json
```

## Project structure

- `pyrepofile/` — package code.
- `tests/` — ad-hoc verification tests.
- `docs/` — usage notes.

## License

MIT

[Source on GitHub](https://github.com/eitanben-ami/pyrepofile)
