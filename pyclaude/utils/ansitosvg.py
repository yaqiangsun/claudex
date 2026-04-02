"""
ANSI to SVG utility.

Convert ANSI terminal output to SVG images.
"""

from typing import Optional


def ansi_to_svg(ansi_text: str, width: int = 80, height: int = 24) -> Optional[str]:
    """Convert ANSI text to SVG."""
    # Simple placeholder implementation
    lines = ansi_text.split('\n')
    svg_lines = ['<svg xmlns="http://www.w3.org/2000/svg">']
    for i, line in enumerate(lines[:height]):
        svg_lines.append(f'<text x="0" y="{i*16+12}">{line}</text>')
    svg_lines.append('</svg>')
    return '\n'.join(svg_lines)


__all__ = ['ansi_to_svg']