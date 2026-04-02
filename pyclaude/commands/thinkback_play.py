"""Thinkback-play command."""
import click

@click.command()
def thinkback_play():
    """Thinkback play command."""
    click.echo("thinkback-play command")

__all__ = ['thinkback_play']