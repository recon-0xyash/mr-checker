from pathlib import Path

from typer.testing import CliRunner

from mrchecker.cli import app
from mrchecker.rules.loader import load_rules
from mrchecker.utils.mask import mask_secret

runner = CliRunner()
rules = load_rules()

aws_rule = next(rule for rule in rules if rule.id == "aws-access-key")

github_rule = next(rule for rule in rules if rule.id == "github-pat")


def test_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0


def test_scan_requires_argument() -> None:
    result = runner.invoke(app, ["scan"])
    assert result.exit_code == 2


def test_scan_valid_file() -> None:
    result = runner.invoke(app, ["scan", str(Path(__file__))])
    assert result.exit_code == 0


def test_scan_invalid_file() -> None:
    result = runner.invoke(app, ["scan", "does-not-exist.txt"])
    assert result.exit_code == 1


def test_scan_directory() -> None:
    result = runner.invoke(app, ["scan", "src"])
    assert result.exit_code == 0
    assert "Files Scanned" in result.stdout
    assert "Mode          : Directory" in result.stdout


def test_scan_empty_file(tmp_path: Path) -> None:
    file = tmp_path / "empty.txt"
    file.write_text("")

    result = runner.invoke(app, ["scan", str(file)])

    assert result.exit_code == 0


def test_scan_text_file(tmp_path: Path) -> None:
    file = tmp_path / "demo.txt"

    file.write_text(
        "Hello\nWorld\nPython",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["scan", str(file)])

    assert result.exit_code == 0


def test_valid_aws_key() -> None:
    assert aws_rule.pattern.search("AKIAABCDEFGHIJKLMNOP")


def test_invalid_prefix() -> None:
    assert aws_rule.pattern.search("AKIBABCDEFGHIJKLMNOP") is None


def test_invalid_case() -> None:
    assert aws_rule.pattern.search("akiaABCDEFGHIJKLMNOP") is None


def test_invalid_length() -> None:
    assert aws_rule.pattern.search("AKIA123") is None


def test_detects_aws_key(tmp_path: Path) -> None:
    file = tmp_path / "secret.txt"

    file.write_text(
        "hello\nAKIAABCDEFGHIJKLMNOP\nworld",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["scan", str(file)])

    assert result.exit_code == 0
    assert "Finding #1" in result.stdout
    assert mask_secret("AKIAABCDEFGHIJKLMNOP") in result.stdout
    assert "aws-access-key" in result.stdout

    # Step 5 checks
    assert "Scan Summary" in result.stdout
    assert "Findings" in result.stdout
    assert "Status" in result.stdout
    assert "SUCCESS" in result.stdout
    assert "Findings" in result.stdout
    assert "1" in result.stdout
    assert "Rule Name" in result.stdout
    assert "Rule ID" in result.stdout
    assert "Category" in result.stdout
    assert "Severity" in result.stdout
    assert "Description" in result.stdout
    assert "Recommendation" in result.stdout

    assert "Cloud" in result.stdout
    assert "Rotate the exposed AWS Access Key immediately." in result.stdout


def test_valid_github_token() -> None:
    assert github_rule.pattern.search("ghp_123456789012345678901234567890123456")


def test_invalid_github_prefix() -> None:
    assert github_rule.pattern.search("ghx_123456789012345678901234567890123456") is None


def test_invalid_github_length() -> None:
    assert github_rule.pattern.search("ghp_123") is None


def test_detects_github_token(tmp_path: Path) -> None:
    file = tmp_path / "github.txt"

    file.write_text(
        "ghp_123456789012345678901234567890123456",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["scan", str(file)],
    )

    assert result.exit_code == 0

    assert "github-pat" in result.stdout
    assert "Source Control" in result.stdout
    assert "Revoke and regenerate" in result.stdout


def test_no_findings(tmp_path: Path) -> None:
    file = tmp_path / "clean.txt"

    file.write_text(
        "hello\nworld",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["scan", str(file)])

    assert result.exit_code == 0

    assert "No secrets detected" in result.stdout
    assert "SUCCESS" in result.stdout
