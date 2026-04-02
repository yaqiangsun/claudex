"""Mock-limits command."""
import click

@click.command()
def mock_limits():
    """Mock limits command."""
    click.echo("mock-limits command")

__all__ = ['mock_limits']