"""Onboarding command."""
import click

@click.command()
def onboarding():
    """Onboarding command."""
    click.echo("onboarding command")

__all__ = ['onboarding']