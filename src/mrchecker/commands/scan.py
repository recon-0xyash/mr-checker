from pathlib import Path

import typer
from rich.console import Console
from rich.rule import Rule

from mrchecker.models.finding import Finding
from mrchecker.rules.loader import load_rules
from mrchecker.source.filesystem import discover_files
from mrchecker.utils.colors import severity_color
from mrchecker.utils.file_reader import read_file
from mrchecker.utils.mask import mask_secret

console = Console()


def scan(
    path: Path = typer.Argument(
        ...,
        help="File or directory to scan.",
    ),
    exclude: list[str] = typer.Option(
        [],
        "--exclude",
        help="Directories or paths to skip.",
    ),
) -> None:
    """
    Scan a single file for secrets.
    """

    target = path.resolve()

    if not target.exists():
        console.print(f"[red]Error:[/red] '{target}' does not exist.")
        raise typer.Exit(code=1)

    if target.is_file():
        files = [target]

    elif target.is_dir():
        files = discover_files(
            target,
            set(exclude),
        )

    else:
        console.print(f"[red]Error:[/red] '{target}' is not a valid file or directory.")
        raise typer.Exit(code=1)
    # ...

    rules = load_rules()

    total_findings = 0
    files_with_findings = 0
    total_lines = 0
    severity_counts = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    console.print(Rule("Scan Configuration"))

    scan_mode = "Directory" if target.is_dir() else "Single File"

    console.print(f"Target        : {target}")
    console.print(f"Mode          : {scan_mode}")
    console.print(f"Rules Loaded  : {len(rules)}")
    console.print(f"Files Found   : {len(files)}")
    console.print("Max File Size : 5 MB")

    if exclude:
        console.print(f"Excludes      : {', '.join(sorted(exclude))}")
    else:
        console.print("Excludes      : Default (.git, __pycache__)")

    console.print()

    for index, file in enumerate(files, start=1):
        lines = read_file(file)
        total_lines += len(lines)

        console.print(Rule(f"Scanning ({index}/{len(files)}): {file.name}"))
        relative = file.relative_to(target) if target.is_dir() else file.name
        console.print(f"Path  : {relative}")
        console.print(f"Lines : {len(lines)}")
        console.print()

        findings: list[Finding] = []

        for line_number, line in enumerate(lines, start=1):
            for rule in rules:
                match = rule.pattern.search(line)

                if match:
                    findings.append(
                        Finding(
                            file=file,
                            line=line_number,
                            rule_id=rule.id,
                            rule_name=rule.name,
                            description=rule.description,
                            category=rule.category,
                            severity=rule.severity,
                            recommendation=rule.recommendation,
                            secret=match.group(),
                        )
                    )
                    severity_counts[rule.severity] += 1

        total_findings += len(findings)

        if not findings:
            console.print("[green]✓ No secrets detected in this file.[/green]")
            console.print()
        else:
            files_with_findings += 1
            for index, finding in enumerate(
                findings,
                start=1,
            ):
                color = severity_color(finding.severity)
                console.print(
                    Rule(
                        f"Finding #{index}",
                        style=color,
                    )
                )

                display_file = (
                    finding.file.relative_to(target) if target.is_dir() else finding.file.name
                )

                console.print(f"File           : {display_file}")

                console.print()

                console.print(f"Rule Name      : {finding.rule_name}")
                console.print(f"Rule ID        : {finding.rule_id}")

                console.print()

                console.print(f"Category       : {finding.category}")

                console.print(f"Severity       : [{color}]{finding.severity.upper()}[/{color}]")

                console.print()

                console.print(f"Line           : {finding.line}")

                console.print(f"Secret         : {mask_secret(finding.secret)}")
                console.print()

                console.print(f"Description    : {finding.description}")

                console.print(f"Recommendation : {finding.recommendation}")

                console.print()
    # TODO:
    # Replace console output with Rich Progress in a future milestone.
    console.print(Rule("Scan Summary"))
    console.print(f"Files Scanned : {len(files)}")
    console.print(f"Files With Findings : {files_with_findings}")
    console.print(f"Lines Scanned : {total_lines}")
    console.print(f"Rules Loaded  : {len(rules)}")
    console.print(f"Findings      : {total_findings}")
    console.print()
    console.print(f"Critical      : {severity_counts['critical']}")
    console.print(f"High          : {severity_counts['high']}")
    console.print(f"Medium        : {severity_counts['medium']}")
    console.print(f"Low           : {severity_counts['low']}")
    console.print()
    console.print("[green]Status[/green]        : [bold green]SUCCESS[/bold green]")
