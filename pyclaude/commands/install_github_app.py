"""Install-github-app command."""
import click

@click.command()
def install_github_app():
    """Install GitHub app command."""
    click.echo("install-github-app command")

__all__ = ['install_github_app']