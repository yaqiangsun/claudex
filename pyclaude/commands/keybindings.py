"""Keybindings command."""
import click

@click.command()
def keybindings():
    """Keybindings command."""
    click.echo("keybindings command")

__all__ = ['keybindings']