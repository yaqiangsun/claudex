"""Feedback command."""
import click

@click.command()
def feedback():
    """Feedback command."""
    click.echo("feedback command")

__all__ = ['feedback']