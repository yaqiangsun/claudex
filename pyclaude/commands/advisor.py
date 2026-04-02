"""Advisor command."""
import click

@click.command()
def advisor():
    """Advisor command."""
    click.echo("advisor command")

__all__ = ['advisor']