"""Summary command."""
import click

@click.command()
def summary():
    """Summary command."""
    click.echo("summary command")

__all__ = ['summary']