"""Stickers command."""
import click

@click.command()
def stickers():
    """Stickers command."""
    click.echo("stickers command")

__all__ = ['stickers']