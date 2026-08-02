# Milestone 02 — Rule-Based Scanning Engine

## Objective

The goal of Milestone 2 was to transform mr-checker from a basic single-file regex scanner into a modular, rule-driven secret scanning engine capable of scanning entire projects. This milestone focused on scalability, maintainability, and creating an architecture that can easily support additional secret detection rules in future releases.

---

## Features Implemented

### Rule Engine

- Introduced a TOML-based rule system for defining secret detection rules.
- Implemented a dynamic rule loader that parses rule definitions at runtime.
- Added support for multiple built-in detection rules.
- Compiled regex patterns only once during loading for improved performance.

---

### Rule Metadata

Each rule now includes structured metadata:

- Rule ID
- Rule Name
- Description
- Category
- Severity
- Recommendation
- Regex Pattern

This separates detection logic from presentation and prepares the project for future report formats.

---

### Finding Model

Replaced simple tuple-based findings with a dedicated `Finding` model.

Each finding now stores:

- File
- Line Number
- Rule ID
- Rule Name
- Category
- Severity
- Description
- Recommendation
- Matched Secret

This creates a consistent data structure that can later be exported to JSON, SARIF, HTML, or Markdown without changing the scanning engine.

---

### Directory Scanning

Implemented recursive directory scanning.

Features include:

- Recursive file discovery
- Single-file mode
- Directory mode
- File filtering
- Maximum file size validation
- Binary file skipping
- Custom exclusion support using `--exclude`

---

### CLI Improvements

Improved the overall scanning experience by adding:

- Scan configuration section
- Per-file scan progress
- Rich finding output
- Relative file paths
- Secret masking
- Severity highlighting
- Scan summary
- Severity statistics

---

### Secret Protection

Implemented masking for detected secrets before displaying them in the console.

Example:

AKIAABCDEFGHIJKLMNOP

↓

AKIA************MNOP

This prevents accidental exposure while still allowing users to identify which credential was detected.

---

### Testing

Expanded the automated test suite to cover:

- Rule loading
- Rule parsing
- Directory scanning
- File discovery
- Secret masking
- CLI behaviour
- Finding generation

All tests successfully pass.

---

### Code Quality

Integrated automated development tooling:

- Ruff
- Ruff Formatter
- MyPy
- Pytest
- Pre-commit Hooks

The project now maintains a consistent coding style and performs automatic quality checks before every commit.

---

## Challenges Faced

One of the largest architectural changes during this milestone was replacing simple tuple-based findings with a structured Finding model. Although this required refactoring multiple components, it significantly improved readability and prepares the scanner for future export formats.

Another challenge involved balancing user-friendly CLI output with maintaining accurate internal data structures, particularly around displaying relative file paths while preserving the original filesystem paths.

Designing the rule system also required separating detection logic from metadata so that rules remain self-contained and extensible.

---

## Lessons Learned

This milestone reinforced several software engineering principles:

- Data models are easier to maintain than loosely structured tuples.
- Separating rule metadata from scanning logic improves extensibility.
- Small incremental refactors reduce debugging effort.
- Automated formatting, linting, and testing greatly improve development confidence.
- Building modular components early makes future milestones significantly easier.

---

## Project Status

At the end of Milestone 2, mr-checker now supports:

- Rule-based scanning
- Multiple detection rules
- Recursive directory scanning
- Rich finding models
- Metadata-driven rule definitions
- Secret masking
- Professional CLI output
- Comprehensive automated testing

The project has evolved from a proof-of-concept scanner into a modular secret scanning framework.

---

## Next Milestone

Milestone 3 will focus on expanding detection capabilities by introducing additional secret rules, improving scanner performance, and laying the groundwork for future reporting formats such as JSON and SARIF.
