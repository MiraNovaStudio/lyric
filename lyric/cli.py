"""
Lyric Language CLI - Compatibility Layer
This module provides backward compatibility for the old 'lyric.cli' module.
All functionality is re-exported from lyric_lang.cli.
"""

# Re-export everything from lyric_lang.cli for backward compatibility
import lyric_lang.cli
from lyric_lang.cli import *

# Ensure main function is available
main = lyric_lang.cli.main
