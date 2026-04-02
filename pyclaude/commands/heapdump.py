"""Heapdump command."""
import click

@click.command()
def heapdump():
    """Heapdump command."""
    click.echo("heapdump command")

__all__ = ['heapdump']