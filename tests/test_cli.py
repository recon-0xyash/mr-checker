from pathlib import Path

from typer.testing import CliRunner

from mrchecker.cli import app

runner = CliRunner()


def test_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0


def test_scan_current_directory() -> None:
    result = runner.invoke(app, ["scan"])
    assert result.exit_code == 0


def test_scan_invalid_directory() -> None:
    result = runner.invoke(app, ["scan", "does-not-exist"])
    assert result.exit_code == 1


def test_scan_file_instead_of_directory() -> None:
    result = runner.invoke(app, ["scan", str(Path(__file__))])
    assert result.exit_code == 1
