"""Color command."""
import click

@click.command()
def color():
    """Color command."""
    click.echo("color command")

__all__ = ['color']