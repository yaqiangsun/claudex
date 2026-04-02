"""Plugin command."""
import click

@click.command()
def plugin():
    """Plugin command."""
    click.echo("plugin command")

__all__ = ['plugin']