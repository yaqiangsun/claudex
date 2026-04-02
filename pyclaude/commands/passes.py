"""Passes command."""
import click

@click.command()
def passes():
    """Passes command."""
    click.echo("passes command")

__all__ = ['passes']