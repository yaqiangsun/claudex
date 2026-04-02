"""Brief command."""
import click

@click.command()
def brief():
    """Brief command."""
    click.echo("brief command")

__all__ = ['brief']