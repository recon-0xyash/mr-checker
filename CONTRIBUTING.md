# Contributing

Thank you for contributing to Mr.Checker.

## Setup

```bash
git clone https://github.com/recon-0xyash/mr-checker

cd mr-checker

python -m venv .venv

pip install -e ".[dev]"
```

## Before every commit

```bash
ruff check .

ruff format .

mypy src

pytest
```

## Commit Messages

Use Conventional Commits.

Examples:

```text
feat: add recursive file scanner

fix: resolve path traversal bug

docs: update README

refactor: simplify scan engine

test: add CLI tests

chore: update dependencies
```
