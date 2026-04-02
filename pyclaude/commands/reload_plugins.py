"""Reload-plugins command."""
import click

@click.command()
def reload_plugins():
    """Reload plugins command."""
    click.echo("reload-plugins command")

__all__ = ['reload_plugins']