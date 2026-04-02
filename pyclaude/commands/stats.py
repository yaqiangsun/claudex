"""Stats command."""
import click

@click.command()
def stats():
    """Stats command."""
    click.echo("stats command")

__all__ = ['stats']