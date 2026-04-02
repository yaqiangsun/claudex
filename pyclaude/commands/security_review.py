"""Security-review command."""
import click

@click.command()
def security_review():
    """Security review command."""
    click.echo("security-review command")

__all__ = ['security_review']