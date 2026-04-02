"""Fast command."""
import click

@click.command()
def fast():
    """Fast command."""
    click.echo("fast command")

__all__ = ['fast']