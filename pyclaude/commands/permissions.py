"""Permissions command."""
import click

@click.command()
def permissions():
    """Permissions command."""
    click.echo("permissions command")

__all__ = ['permissions']