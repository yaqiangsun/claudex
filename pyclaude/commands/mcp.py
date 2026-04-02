"""MCP command."""
import click

@click.command()
def mcp():
    """MCP command."""
    click.echo("mcp command")

__all__ = ['mcp']