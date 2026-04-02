"""Hooks command."""
import click

@click.command()
def hooks():
    """Hooks command."""
    click.echo("hooks command")

__all__ = ['hooks']