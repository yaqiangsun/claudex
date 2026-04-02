"""Bridge-kick command."""
import click

@click.command()
def bridge_kick():
    """Bridge kick command."""
    click.echo("bridge-kick command")

__all__ = ['bridge_kick']