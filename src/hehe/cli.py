import typer
from hehe.commands.find import find
from hehe.commands.show import show
from hehe.commands.diff import diff

app = typer.Typer(
    name="hehe",
    help="A configuration analysis and security tool.",
    no_args_is_help=True
)
@app.callback()
def callback():
    """hehe - Configuration analysis and security tool."""
    pass

@app.command()
def version():
    """Show hehe version"""
    typer.echo("hehe 0.0.1")

app.command("find")(find)
app.command("show")(show)
app.command("diff")(diff)
def main():
    app()