"""Remote-env command."""
import click

@click.command()
def remote_env():
    """Remote env command."""
    click.echo("remote-env command")

__all__ = ['remote_env']