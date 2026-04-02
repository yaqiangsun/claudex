"""Remote-setup command."""
import click

@click.command()
def remote_setup():
    """Remote setup command."""
    click.echo("remote-setup command")

__all__ = ['remote_setup']