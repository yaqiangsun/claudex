"""Release-notes command."""
import click

@click.command()
def release_notes():
    """Release notes command."""
    click.echo("release-notes command")

__all__ = ['release_notes']