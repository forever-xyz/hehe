from pathlib import Path

import typer

from hehe.core.lint import lint_configs
from hehe.ui import title, success, file_title


def lint(
    path: Path = typer.Argument(
        Path("."),
        help="Directory to lint",
    ),
    file_type: str | None = typer.Option(
        None,
        "--type",
        "-t",
        help="Filter by config type",
    ),
    exclude: list[str] | None = typer.Option(
        None,
        "--exclude",
        "-e",
        help="Directory to exclude",
    ),
):
    """Check configuration files for common problems."""

    root = path.resolve()

    if not root.exists():
        typer.secho(
            f"❌ Path not found: {root}",
            fg=typer.colors.RED,
            bold=True,
            err=True,
        )
        raise typer.Exit(code=1)

    exclude_dirs = set(exclude) if exclude else None

    issues = lint_configs(
        root=root,
        file_type=file_type,
        exclude_dirs=exclude_dirs,
    )

    title("Configuration Lint", "🧹")

    if not issues:
        success("No configuration problems found.")
        return

    error_count = sum(
        1
        for issue in issues
        if issue.level == "ERROR"
    )

    warning_count = sum(
        1
        for issue in issues
        if issue.level == "WARN"
    )

    typer.secho(
        f"❌ Errors: {error_count}",
        fg=typer.colors.RED,
        bold=True,
    )

    typer.secho(
        f"⚠️  Warnings: {warning_count}",
        fg=typer.colors.YELLOW,
        bold=True,
    )

    typer.echo()

    current_file: Path | None = None

    for issue in issues:

        # 同一个文件只显示一次文件名
        if issue.file != current_file:

            if current_file is not None:
                typer.echo()

            relative_path = issue.file.relative_to(root)

            file_title(str(relative_path))
            typer.echo()

            current_file = issue.file

        # ERROR
        if issue.level == "ERROR":

            # 有具体配置 Key
            if issue.key:
                typer.secho(
                    f"  ❌ {issue.key}",
                    fg=typer.colors.RED,
                    bold=True,
                )

                typer.echo(
                    f"      {issue.message}"
                )

            # 没有具体 Key，例如整个文件解析失败
            else:
                typer.secho(
                    f"  ❌ ERROR  {issue.message}",
                    fg=typer.colors.RED,
                    bold=True,
                )

        # WARN
        else:
            typer.secho(
                f"  ⚠️  {issue.key}",
                fg=typer.colors.YELLOW,
                bold=True,
            )

            typer.echo(
                f"      {issue.message}"
            )

    typer.echo()