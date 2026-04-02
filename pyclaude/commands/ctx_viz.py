"""Ctx_viz command."""
import click

@click.command()
def ctx_viz():
    """Context visualization command."""
    click.echo("ctx_viz command")

__all__ = ['ctx_viz']