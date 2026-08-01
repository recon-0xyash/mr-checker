from pathlib import Path

import typer


def read_file(file: Path) -> list[str]:
    """
    Read a text file and return its contents as a list of lines.
    """

    try:
        with file.open(
            mode="r",
            encoding="utf-8",
        ) as f:
            return f.readlines()

    except UnicodeDecodeError:
        typer.echo("Error: File is not valid UTF-8.")
        raise typer.Exit(code=1) from None

    except PermissionError:
        typer.echo("Error: Permission denied.")
        raise typer.Exit(code=1) from None

    except OSError as exc:
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=1) from None
