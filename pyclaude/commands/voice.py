"""Voice command."""
import click

@click.command()
def voice():
    """Voice command."""
    click.echo("voice command")

__all__ = ['voice']