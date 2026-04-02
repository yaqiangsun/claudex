"""Skills command."""
import click

@click.command()
def skills():
    """Skills command."""
    click.echo("skills command")

__all__ = ['skills']