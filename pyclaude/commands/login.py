"""Login command."""
import click

@click.command()
def login():
    """Login command."""
    click.echo("login command")

__all__ = ['login']