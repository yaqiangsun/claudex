"""Good-claude command."""
import click

@click.command()
def good_claude():
    """Good claude command."""
    click.echo("good-claude command")

__all__ = ['good_claude']