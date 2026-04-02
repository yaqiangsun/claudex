"""Insights command."""
import click

@click.command()
def insights():
    """Insights command."""
    click.echo("insights command")

__all__ = ['insights']