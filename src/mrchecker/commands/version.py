import platform

# import typer
from rich.console import Console
from rich.table import Table

from mrchecker import __version__

console = Console()


def version() -> None:
    """Display version information."""

    table = Table(title="Mr.Checker")

    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Version", __version__)
    table.add_row("Python", platform.python_version())
    table.add_row(
        "Platform",
        f"{platform.system()} {platform.release()}",
    )

    console.print(table)
