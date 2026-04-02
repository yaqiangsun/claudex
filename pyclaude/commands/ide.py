"""IDE command."""
import click

@click.command()
def ide():
    """IDE command."""
    click.echo("ide command")

__all__ = ['ide']