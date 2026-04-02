"""Break-cache command."""
import click

@click.command()
def break_cache():
    """Break cache command."""
    click.echo("break-cache command")

__all__ = ['break_cache']