from pathlib import Path

import typer
from rich.console import Console
from rich.rule import Rule

from mrchecker.utils.file_reader import read_file
from mrchecker.utils.regex import AWS_ACCESS_KEY_PATTERN

console = Console()


def scan(
    file: Path = typer.Argument(
        ...,
        help="File to scan.",
    ),
) -> None:
    """
    Scan a single file for secrets.
    """

    target = file.resolve()

    if not target.exists():
        console.print(f"[red]Error:[/red] '{target}' does not exist.")
        raise typer.Exit(code=1)

    if not target.is_file():
        console.print(f"[red]Error:[/red] '{target}' is not a file.")
        raise typer.Exit(code=1)
    # ...

    lines = read_file(target)

    console.print("[green]✓[/green] File accepted")
    console.print(f"Target file: [cyan]{target}[/cyan]")
    console.print(f"Lines read: [yellow]{len(lines)}[/yellow]")

    findings: list[tuple[int, str]] = []

    for line_number, line in enumerate(lines, start=1):
        match = AWS_ACCESS_KEY_PATTERN.search(line)

        if match:
            findings.append(
                (
                    line_number,
                    match.group(),
                )
            )

    if not findings:
        console.print("[green]No AWS Access Keys detected.[/green]")
        console.print()
    else:
        for index, (line_number, secret) in enumerate(
            findings,
            start=1,
        ):
            console.print(f"[bold]Finding #{index}[/bold]")
            console.print(f"Line  : {line_number}")
            console.print(f"Match : {secret}")
            console.print()

    console.print(Rule("Scan Summary"))
    console.print(f"File     : {target.name}")
    console.print(f"Lines    : {len(lines)}")
    console.print(f"Findings : {len(findings)}")
    console.print("[green]Status[/green]   : SUCCESS")
