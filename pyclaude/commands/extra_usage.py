"""Extra-usage command."""
import click

@click.command()
def extra_usage():
    """Extra usage command."""
    click.echo("extra-usage command")

__all__ = ['extra_usage']