"""Mobile command."""
import click

@click.command()
def mobile():
    """Mobile command."""
    click.echo("mobile command")

__all__ = ['mobile']