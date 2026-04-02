"""CreateMovedToPluginCommand."""
import click

@click.command()
def create_moved_to_plugin_command():
    """Create moved to plugin command."""
    click.echo("createMovedToPluginCommand")

__all__ = ['create_moved_to_plugin_command']