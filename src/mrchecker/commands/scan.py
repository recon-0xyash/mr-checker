from pathlib import Path

import typer
from rich.console import Console

console = Console()


def scan(
    path: Path = typer.Argument(
        Path("."),
        help="Directory to scan.",
    ),
) -> None:
    """
    Scan a directory for secrets.
    """

    target = path.resolve()

    if not target.exists():
        console.print(f"[red]Error:[/red] '{target}' does not exist.")
        raise typer.Exit(code=1)

    if not target.is_dir():
        console.print(f"[red]Error:[/red] '{target}' is not a directory.")
        raise typer.Exit(code=1)

    console.print("[green]✓[/green] Scan initialized")
    console.print(f"Target directory: [cyan]{target}[/cyan]")
    console.print()
    console.print("[yellow]Secret detection engine is not implemented yet.[/yellow]")
