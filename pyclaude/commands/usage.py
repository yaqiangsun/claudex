"""Usage command."""
import click

@click.command()
def usage():
    """Usage command."""
    click.echo("usage command")

__all__ = ['usage']