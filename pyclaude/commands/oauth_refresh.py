"""Oauth-refresh command."""
import click

@click.command()
def oauth_refresh():
    """OAuth refresh command."""
    click.echo("oauth-refresh command")

__all__ = ['oauth_refresh']