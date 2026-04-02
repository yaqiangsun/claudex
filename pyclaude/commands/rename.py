"""Rename command."""
import click

@click.command()
def rename():
    """Rename command."""
    click.echo("rename command")

__all__ = ['rename']