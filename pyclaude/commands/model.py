"""Model command."""
import click

@click.command()
def model():
    """Model command."""
    click.echo("model command")

__all__ = ['model']