"""Plan command."""
import click

@click.command()
def plan():
    """Plan command."""
    click.echo("plan command")

__all__ = ['plan']