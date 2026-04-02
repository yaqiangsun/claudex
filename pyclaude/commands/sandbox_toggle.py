"""Sandbox-toggle command."""
import click

@click.command()
def sandbox_toggle():
    """Sandbox toggle command."""
    click.echo("sandbox-toggle command")

__all__ = ['sandbox_toggle']