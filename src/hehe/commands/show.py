from pathlib import Path
import typer
from hehe.core.parser import parse_config_file
from hehe.core.scanner import get_config_type

def show(path: Path = typer.Argument(
    ...,
    help="Configuration file to display."
)):
    """Show parsed configuration."""
    try:
        config = parse_config_file(path)
    except (FileNotFoundError, ValueError) as exc:
        typer.echo(f"Error:{exc}", err=True)
        raise typer.Exit(code=1)

    config_type = get_config_type(path)

    typer.echo(f"Configuration: {path.name}")
    typer.echo(f"Type: {config_type.upper()}")
    typer.echo(f"keys:{len(config)}")
    typer.echo()

    if not config:
        typer.echo("No configuration entries found.")
        return

    # 找到最长 key，用于输出对齐
    key_width = max(len(key) for key in config)
    for key, value in config.items():
        typer.echo(f"{key:<{key_width}}     {value}")