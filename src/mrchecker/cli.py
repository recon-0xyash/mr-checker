import typer

from mrchecker.commands.scan import scan
from mrchecker.commands.version import version

app = typer.Typer(
    help="A modern secret scanner for developers.",
    no_args_is_help=True,
)

app.command(help="Scan a directory for secrets.")(scan)
app.command(help="Display version information.")(version)

if __name__ == "__main__":
    app()
