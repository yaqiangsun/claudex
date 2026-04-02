"""Bughunter command."""
import click

@click.command()
def bughunter():
    """Bughunter command."""
    click.echo("bughunter command")

__all__ = ['bughunter']