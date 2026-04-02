"""Rate-limit-options command."""
import click

@click.command()
def rate_limit_options():
    """Rate limit options command."""
    click.echo("rate-limit-options command")

__all__ = ['rate_limit_options']