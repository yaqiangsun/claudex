"""Backfill-sessions command."""
import click

@click.command()
def backfill_sessions():
    """Backfill sessions command."""
    click.echo("backfill-sessions command")

__all__ = ['backfill_sessions']