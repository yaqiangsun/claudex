"""Vim command."""
import click

@click.command()
def vim():
    """Vim command."""
    click.echo("vim command")

__all__ = ['vim']