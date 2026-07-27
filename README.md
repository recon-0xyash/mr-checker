# Mr.Checker

> A modern, open-source secret scanner for developers.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![License](https://img.shields.io/badge/License-AGPL--3.0-success)
![Status](https://img.shields.io/badge/Status-Alpha-orange)

---

## Overview

Mr.Checker is a modern command-line secret scanner built in Python.

The goal is to detect accidentally committed secrets before they reach production systems.

This project is being built from scratch as an educational and production-quality cybersecurity tool.

---

## Features

- Fast command-line interface
- Modern Python architecture
- Recursive repository scanning *(coming soon)*
- Secret detection engine *(coming soon)*
- Rich terminal output
- Cross-platform support
- Extensible architecture

---

## Installation

### User

```bash
pip install mr-checker
```

### Developer

```bash
git clone https://github.com/recon-0xyash/mr-checker

cd mr-checker

python -m venv .venv

pip install -e ".[dev]"
```

---

## Usage

```bash
mrchecker --help

mrchecker version

mrchecker scan .
```

---

## Development

Run quality checks

```bash
ruff check .

ruff format --check .

mypy src

pytest
```

---

## Project Structure

```text
src/
└── mrchecker/
    ├── commands/
    ├── core/
    ├── utils/
    ├── cli.py
    └── __main__.py
```

---

## Roadmap

- Project foundation
- Recursive file discovery
- Ignore engine
- Regex detection
- Entropy detection
- Report generation
- Plugin system

---

## Contributing

Contributions are welcome.

Please read **CONTRIBUTING.md** before opening a Pull Request.

---

## License

Licensed under the GNU Affero General Public License v3.0.
