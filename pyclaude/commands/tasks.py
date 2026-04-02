"""Tasks command."""
import click

@click.command()
def tasks():
    """Tasks command."""
    click.echo("tasks command")

__all__ = ['tasks']