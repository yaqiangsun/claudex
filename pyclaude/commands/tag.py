"""Tag command."""
import click

@click.command()
def tag():
    """Tag command."""
    click.echo("tag command")

__all__ = ['tag']