"""Ant-trace command."""
import click

@click.command()
def ant_trace():
    """Ant trace command."""
    click.echo("ant-trace command")

__all__ = ['ant_trace']