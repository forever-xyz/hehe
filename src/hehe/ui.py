import typer


def title(text: str, icon: str = "🔍") -> None:
    typer.secho(
        f"\n{icon} {text}",
        fg=typer.colors.CYAN,
        bold=True,
    )


def success(text: str) -> None:
    typer.secho(
        f"✅ {text}",
        fg=typer.colors.GREEN,
        bold=True,
    )


def warning(text: str) -> None:
    typer.secho(
        f"⚠️  {text}",
        fg=typer.colors.YELLOW,
    )


def error(text: str) -> None:
    typer.secho(
        f"❌ {text}",
        fg=typer.colors.RED,
    )


def file_title(path: str) -> None:
    typer.secho(
        f"📄 {path}",
        fg=typer.colors.YELLOW,
        bold=True,
    )