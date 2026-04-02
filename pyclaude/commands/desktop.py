"""Desktop command."""
import click

@click.command()
def desktop():
    """Desktop command."""
    click.echo("desktop command")

__all__ = ['desktop']