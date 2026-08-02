# Development Diary — Milestone 1
## Version
v0.2.0

## Duration
Project Foundation → First Working Secret Scanner

---

# Objective

The objective of Milestone 1 was not to build a feature-rich secret scanner.

Instead, the goal was to establish a solid engineering foundation by implementing one complete end-to-end scanning pipeline:

CLI → File Validation → File Reading → Secret Detection → Findings → Summary

By deliberately limiting the scope, every design decision could be understood and verified before introducing additional complexity.

---

# What Was Implemented

## CLI

Implemented the first installable CLI using Typer.

Commands:

- mrchecker scan
- mrchecker version

The CLI can now be installed locally using:

pip install -e .

and executed as

mrchecker scan

instead of

python main.py

This establishes Mr.Checker as an actual command-line application rather than a collection of Python scripts.

---

## File Validation

Implemented validation for:

- Missing files
- Invalid paths
- Directory passed instead of file

Errors intentionally return friendly messages rather than Python tracebacks.

Example:

Error: "example.txt" does not exist.

---

## File Reader

Created a dedicated utility responsible for reading files.

Responsibilities:

- UTF-8 decoding
- Permission handling
- OS errors
- Returning file contents

The scanner itself never performs file I/O directly.

This separation makes future testing and reuse significantly easier.

---

## Detection

Implemented the first detection rule:

AWS Access Keys

Pattern:

AKIA[0-9A-Z]{16}

The detection rule is stored separately from the CLI implementation.

This separation allows future milestones to introduce additional rules without modifying command logic.

---

## Findings

Instead of immediately printing matches, findings are first collected.

Current representation:

(Line Number, Secret)

Although simple, this design choice prepares the project for:

- JSON reports
- SARIF
- Confidence scoring
- Baseline suppression
- Live validation

without changing the detection pipeline.

---

## Output

Implemented human-readable terminal output.

Displays:

- File accepted
- File path
- Total lines
- Individual findings
- Scan summary

Current summary contains:

- File
- Lines scanned
- Total findings
- Scan status

---

## Testing

Implemented both unit and integration testing.

Unit tests validate:

- AWS regex
- Invalid prefixes
- Invalid length
- Invalid casing

Integration tests validate:

- CLI execution
- Empty files
- Missing files
- Directory input
- Secret detection
- Clean files
- Summary output

This milestone established the project's testing philosophy:

Every feature should be testable independently.

---

## Tooling

Configured:

- Ruff
- MyPy
- Pytest
- Pre-commit hooks
- GitHub Actions CI

The repository now enforces formatting, linting and static analysis before commits are accepted.

---

# Engineering Decisions

## Why only one detection rule?

Because the objective was validating the architecture—not maximizing functionality.

If one rule cannot be implemented cleanly, fifty rules will only create technical debt.

---

## Why collect findings before printing?

Printing immediately makes later reporting difficult.

Collecting findings first enables future features without redesigning the scanner.

---

## Why separate file reading?

Reading files is an independent responsibility.

Keeping file I/O separate simplifies testing and future extension.

---

## Why compile regexes?

Compiled regular expressions are reused during scanning and avoid recompilation for every line.

This is both more efficient and easier to organize.

---

## Why Typer?

Typer provides:

- Type-safe CLI definitions
- Automatic help generation
- Shell completion
- Clean command organization

while remaining lightweight.

---

# Challenges Encountered

Several implementation issues were intentionally resolved instead of ignored.

Examples include:

- Proper CLI packaging
- Editable installs
- Ruff formatting rules
- Exception chaining using `raise ... from None`
- MyPy strict typing
- Pre-commit hook failures
- Git tagging mistakes
- Repository release workflow

Resolving these issues strengthened the project foundation.

---

# Lessons Learned

A reliable CLI tool depends more on architecture than on the number of implemented features.

Early investment in testing, linting, typing and project structure significantly reduces future maintenance cost.

The project should evolve through small, verified milestones rather than large feature dumps.

---

# Repository Status

Current capabilities:

✓ Installable CLI

✓ Single-file scanning

✓ AWS Access Key detection

✓ Structured findings

✓ Scan summary

✓ Automated testing

✓ Static analysis

✓ CI-ready repository

---

# Deferred Features

The following were intentionally postponed:

- Directory scanning
- Recursive traversal
- Ignore rules
- Multiple secret providers
- Rule registry
- Entropy detection
- JSON reports
- SARIF reports
- Baseline suppression
- Live credential validation
- Parallel scanning

These belong to future milestones.

---

# Overall Evaluation

Milestone 1 successfully established the technical foundation for Mr.Checker.

Although the scanner currently detects only a single secret type, every major architectural layer required for future development now exists.

Future milestones will extend these layers rather than replace them.

No architectural redesign is expected before v1.0.

---

# Next Milestone

Milestone 2 will transition from scanning a single file to scanning complete directory structures while preserving the architecture established during Milestone 1.
