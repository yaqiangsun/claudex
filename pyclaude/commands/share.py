"""Share command."""
import click

@click.command()
def share():
    """Share command."""
    click.echo("share command")

__all__ = ['share']