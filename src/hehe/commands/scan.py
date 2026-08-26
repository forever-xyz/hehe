from pathlib import Path
import typer
from hehe.core.scan import scan_sensitive_configs

def scan(
        path: Path = typer.Argument(
            Path("."),
            help="Directory to scan."
        ),
        file_type: str | None = typer.Option(
            None,
            "--type",
            "-t",
            help="Filter by config type."
        ),
        exclude: list[str] | None = typer.Option(
            None,
            "--exclude",
            "-e",
            help="Directory to exclude.",
        )
):
    """Scan configuration files for sensitive values."""
    root = path.resolve()

    if not root.exists():
        typer.secho(
            f"Error: path not found: {root}",
            fg=typer.colors.RED,
            err=True
        )
        raise typer.Exit(code=1)

    exclude_dirs = set(exclude) if exclude else None

    findings = scan_sensitive_configs(
        root=root,
        file_type=file_type,
        exclude_dirs=exclude_dirs
    )

    typer.secho(
        "\nSensitive Configuration Scan",
        fg=typer.colors.CYAN,
        bold=True,
    )

    typer.echo(f"Found {len(findings)} sensitive configuration item(s)\n")

    if not findings:
        typer.secho("No sensitive configuration found.", fg=typer.colors.GREEN)
        return

    current_file: Path | None = None

    for finding in findings:
        if finding.file != current_file:
            if current_file is not None:
                typer.echo()

            relative_path = finding.file.relative_to(root)
            typer.secho(
                str(relative_path),
                fg=typer.colors.YELLOW,
                bold=True
            )

            current_file = finding.file

        typer.secho(
            f"  ! {finding.key}",
            fg=typer.colors.RED,
            bold=True
        )
        typer.echo(f"  {finding.value}")

    typer.echo()