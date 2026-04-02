"""Migrations module."""
from .migrate_legacy_opus import migrate_legacy_opus_to_current

__all__ = ['migrate_legacy_opus_to_current']