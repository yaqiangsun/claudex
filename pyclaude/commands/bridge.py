"""Bridge command."""
import click

@click.command()
@click.option('--port', default=8080, help='Port number')
def bridge(port):
    """Bridge command."""
    click.echo(f"bridge command on port {port}")

__all__ = ['bridge']