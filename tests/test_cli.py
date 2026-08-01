from pathlib import Path

from typer.testing import CliRunner

from mrchecker.cli import app
from mrchecker.utils.regex import AWS_ACCESS_KEY_PATTERN

runner = CliRunner()


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
    assert result.exit_code == 1


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
    assert AWS_ACCESS_KEY_PATTERN.search("AKIAABCDEFGHIJKLMNOP")


def test_invalid_prefix() -> None:
    assert AWS_ACCESS_KEY_PATTERN.search("AKIBABCDEFGHIJKLMNOP") is None


def test_invalid_case() -> None:
    assert AWS_ACCESS_KEY_PATTERN.search("akiaABCDEFGHIJKLMNOP") is None


def test_invalid_length() -> None:
    assert AWS_ACCESS_KEY_PATTERN.search("AKIA123") is None


def test_detects_aws_key(tmp_path: Path) -> None:
    file = tmp_path / "secret.txt"

    file.write_text(
        "hello\nAKIAABCDEFGHIJKLMNOP\nworld",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["scan", str(file)])

    assert result.exit_code == 0
    assert "Finding #1" in result.stdout
    assert "AKIAABCDEFGHIJKLMNOP" in result.stdout

    # Step 5 checks
    assert "Scan Summary" in result.stdout
    assert "Findings" in result.stdout
    assert "Status" in result.stdout
    assert "SUCCESS" in result.stdout
    assert "Findings : 1" in result.stdout


def test_no_findings(tmp_path: Path) -> None:
    file = tmp_path / "clean.txt"

    file.write_text(
        "hello\nworld",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["scan", str(file)])

    assert result.exit_code == 0
    assert "No AWS Access Keys detected." in result.stdout

    # Step 5 checks
    assert "Scan Summary" in result.stdout
    assert "Findings" in result.stdout
    assert "Status" in result.stdout
    assert "SUCCESS" in result.stdout
    assert "Findings : 0" in result.stdout
