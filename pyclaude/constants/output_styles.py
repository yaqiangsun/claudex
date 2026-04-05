"""Output styles constants."""

OUTPUT_STYLES = {
    'default': 'Default output style',
    'minimal': 'Minimal output',
    'verbose': 'Verbose output',
    'compact': 'Compact output',
}


def get_output_style(name: str) -> str:
    """Get output style by name."""
    return OUTPUT_STYLES.get(name, OUTPUT_STYLES['default'])


__all__ = ['OUTPUT_STYLES', 'get_output_style']