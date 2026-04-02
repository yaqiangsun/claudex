"""Env command."""
import click

@click.command()
def env():
    """Environment command."""
    click.echo("env command")

__all__ = ['env']