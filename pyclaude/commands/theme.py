"""Theme command."""
import click

@click.command()
def theme():
    """Theme command."""
    click.echo("theme command")

__all__ = ['theme']