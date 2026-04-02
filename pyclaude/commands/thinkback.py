"""Thinkback command."""
import click

@click.command()
def thinkback():
    """Thinkback command."""
    click.echo("thinkback command")

__all__ = ['thinkback']