"""TerminalSetup command."""
import click

@click.command()
def terminal_setup():
    """Terminal setup command."""
    click.echo("terminalSetup command")

__all__ = ['terminal_setup']