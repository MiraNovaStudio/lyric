"""Error classes for Lyric language."""

class LexError(Exception):
    """Raised when lexing fails."""
    pass

class ParseError(Exception):
    """Raised when parsing fails."""
    pass

class RuntimeErrorLyric(Exception):
    """Raised when runtime execution fails."""
    pass
