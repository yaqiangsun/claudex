"""Install-slack-app command."""
import click

@click.command()
def install_slack_app():
    """Install Slack app command."""
    click.echo("install-slack-app command")

__all__ = ['install_slack_app']