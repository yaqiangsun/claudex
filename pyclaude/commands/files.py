"""Files command."""
import click

@click.command()
def files():
    """Files command."""
    click.echo("files command")

__all__ = ['files']