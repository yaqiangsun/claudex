"""Review command."""
import click

@click.command()
def review():
    """Review command."""
    click.echo("review command")

__all__ = ['review']