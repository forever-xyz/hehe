from pathlib import Path
import typer

from hehe.core.check import check_configs
from hehe.core.parser import parse_config_file

def check(
        first_file: Path=typer.Argument(..., help="First configuration file."),
        second_file: Path=typer.Argument(..., help="Second configuration file")
):
    """Check configuration completeness."""

    try:
        first_config = parse_config_file(first_file)
        second_config = parse_config_file(second_file)

    except (FileNotFoundError, ValueError) as ex:
        typer.secho(
            f"Error: {ex}",
            fg=typer.colors.RED,
            err=True
        )
        raise typer.Exit(code=1)

    result = check_configs(
        first_config,
        second_config
    )

    typer.secho(
        "\nConfiguration Check",
        fg=typer.colors.CYAN,
        bold=True,
    )

    typer.echo(f"{first_file.name} <-> {second_file.name}\n")

    total_missing = (len(result.missing_in_first) + len(result.missing_in_second))

    if total_missing == 0:
        typer.secho(
            "Configuration keys are consistent.",
            fg=typer.colors.GREEN,
            bold=True,
        )

        typer.echo(f"Shared keys: {result.shared_count}")

        return

    if result.missing_in_second:
        typer.secho(
            f"Missing in {second_file.name} "
            f"({len(result.missing_in_second)})",
            fg=typer.colors.RED,
            bold=True,
        )

        for key in result.missing_in_second:
            typer.secho(f"  - {key}", fg=typer.colors.RED)

        typer.echo()

    if result.missing_in_first:
        typer.secho(
            f"Missing in {first_file.name} "
            f"({len(result.missing_in_first)})",
            fg=typer.colors.YELLOW,
            bold=True,
        )

        for key in result.missing_in_first:
            typer.secho(f"  - {key}", fg=typer.colors.YELLOW)

        typer.echo()

    typer.echo(f"Shared keys: {result.shared_count}")
    typer.echo(f"Total missing: {total_missing}")