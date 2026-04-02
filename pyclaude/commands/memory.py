"""Memory command."""
import click

@click.command()
def memory():
    """Memory command."""
    click.echo("memory command")

__all__ = ['memory']