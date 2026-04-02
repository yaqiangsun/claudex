"""Chrome command."""
import click

@click.command()
def chrome():
    """Chrome command."""
    click.echo("chrome command")

__all__ = ['chrome']