"""Add-dir command."""
import click

@click.command()
def add_dir():
    """Add directory command."""
    click.echo("add-dir command")

__all__ = ['add_dir']