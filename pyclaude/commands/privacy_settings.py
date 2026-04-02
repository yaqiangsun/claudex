"""Privacy-settings command."""
import click

@click.command()
def privacy_settings():
    """Privacy settings command."""
    click.echo("privacy-settings command")

__all__ = ['privacy_settings']