"""Cost command."""
import click

@click.command()
def cost():
    """Cost command."""
    click.echo("cost command")

__all__ = ['cost']