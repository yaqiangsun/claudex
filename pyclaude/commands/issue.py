"""Issue command."""
import click

@click.command()
def issue():
    """Issue command."""
    click.echo("issue command")

__all__ = ['issue']