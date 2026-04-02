"""Teleport command."""
import click

@click.command()
def teleport():
    """Teleport command."""
    click.echo("teleport command")

__all__ = ['teleport']