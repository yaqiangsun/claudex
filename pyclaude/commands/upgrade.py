"""Upgrade command."""
import click

@click.command()
def upgrade():
    """Upgrade command."""
    click.echo("upgrade command")

__all__ = ['upgrade']