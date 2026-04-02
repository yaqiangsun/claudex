"""Session command."""
import click

@click.command()
def session():
    """Session command."""
    click.echo("session command")

__all__ = ['session']