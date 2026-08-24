from pathlib import Path
import typer

from hehe.core.diff import compare_configs
from hehe.core.parser import parse_config_file

def diff(
        old_file: Path = typer.Argument(..., help="Base configuration file."),
        new_file: Path = typer.Argument(..., help="Configuration file to compare.")
):
    """Compare two configuration files."""
    try:
        old_config = parse_config_file(old_file)
        new_config = parse_config_file(new_file)
    except (FileNotFoundError, ValueError) as ext:
        typer.secho(f"Error: {ext}", err=True)
        raise typer.Exit(code=1)

    result = compare_configs(old_config, new_config)

    # 顶部信息
    typer.secho(f"\nCompare: {old_file.name} -> {new_file.name}", fg= typer.colors.CYAN, bold=True)
    typer.echo(
        f"Changed: {len(result.changed)}  "
        f"Added: {len(result.added)}  "
        f"Removed: {len(result.removed)}"
    )

    typer.echo()
    if(not result.added and not result.removed and not result.changed):
        typer.secho("No differences found.", fg=typer.colors.GREEN,)
        return

    # Changed
    if result.changed:
        typer.secho(
            f"Changed ({len(result.changed)})",
            fg=typer.colors.YELLOW,
            bold=True,
        )

        for change in result.changed:
            # 配置 Key
            typer.secho(
                f"  ~ {change.key}",
                fg=typer.colors.CYAN,
                bold=True,
            )

            # 旧值
            typer.secho(
                f"    OLD  {change.old_value}",
                fg=typer.colors.RED,
            )

            # 新值
            typer.secho(
                f"    NEW  {change.new_value}",
                fg=typer.colors.GREEN,
            )

            typer.echo()

    # Added
    if result.added:
        typer.secho(
            f"Added ({len(result.added)})",
            fg=typer.colors.GREEN,
            bold=True,
        )

        for key, value in result.added.items():
            typer.secho(
                f"  + {key}",
                fg=typer.colors.GREEN,
                bold=True,
            )
            typer.echo(f"    {value}")

        typer.echo()

    # Removed
    if result.removed:
        typer.secho(
            f"Removed ({len(result.removed)})",
            fg=typer.colors.RED,
            bold=True,
        )

        for key, value in result.removed.items():
            typer.secho(
                f"  - {key}",
                fg=typer.colors.RED,
                bold=True,
            )

            typer.echo(f"    {value}")

        typer.echo()