"""Logout command."""
import click

@click.command()
def logout():
    """Logout command."""
    click.echo("logout command")

__all__ = ['logout']