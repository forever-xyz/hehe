from pathlib import Path
import typer
from hehe.core.search import search_configs

def search(
        keyword: str = typer.Argument(
            ...,
            help="Keyword to search."
        ),
        path: Path = typer.Argument(
            Path("."),
            help="Directory to search."
        ),
        file_type: str | None = typer.Option(
            None,
            "--type",
            "-t",
            help="Filter by config type."
        ),
        exclude: list[str] = typer.Option(
            None,
            "--exclude",
            "-e",
            help="Directory to exclude."
        )
):
    """Search configuration keys and values."""

    root = path.resolve()
    if not root.exists():
        typer.secho(
            f"Error: path not found: {root}",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)

    exclude_dirs = set(exclude) if exclude else None

    matches = search_configs(
        root=root,
        keyword=keyword,
        file_type=file_type,
        exclude_dirs=exclude_dirs
    )

    typer.secho(
        f"\nSearch: {keyword}",
        fg=typer.colors.CYAN,
        bold=True
    )
    typer.echo(f"Found {len(matches)} match(es)\n")

    if not matches:
        typer.secho(
            "No matches found",
            fg=typer.colors.YELLOW
        )

    current_file: Path | None = None

    for match in matches:

        if match.file != current_file:
            if current_file is not None:
                typer.echo()

            relative_path = match.file.relative_to(root)

            typer.secho(
                str(relative_path),
                fg=typer.colors.YELLOW,
                bold=True
            )
            current_file = match.file

        typer.secho(f"  {match.key}", fg=typer.colors.CYAN)
        typer.echo(f"   {match.value}")

    typer.echo()