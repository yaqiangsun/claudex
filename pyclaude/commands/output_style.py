"""Output-style command."""
import click

@click.command()
def output_style():
    """Output style command."""
    click.echo("output-style command")

__all__ = ['output_style']