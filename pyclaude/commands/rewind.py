"""Rewind command."""
import click

@click.command()
def rewind():
    """Rewind command."""
    click.echo("rewind command")

__all__ = ['rewind']