from pathlib import Path
import typer
from hehe.core.scanner import scan_config_files

def find(
        path:Path = typer.Argument(Path("."), help="Directory to scan."),
        file_type: str | None = typer.Option(
            None,
            "--type",
            "-t",
            help="Filter by config type.",
        ),
        exclude: list[str] | None = typer.Option(
            None,
            "--exclude",
            "-ec",
            help="Directory to exclude from scanning.",
        )
):
    """Find configuration files."""
    root = path.resolve()

    exclude_dirs = set(exclude) if exclude else None

    files = scan_config_files(root, file_type, exclude_dirs)

    if not files:
        typer.echo("No configuration files found.")
        return

    typer.echo(f"Found {len(files)} configuration file(s):\n")

    for file in files:
        typer.echo(f"{file.relative_to(root)}")