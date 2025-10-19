"""
Lyric Language Error Classes
Defines custom exceptions for lexing, parsing, and runtime errors.
"""


class LexError(Exception):
    """Raised when lexical analysis encounters an error."""
    pass


class ParseError(Exception):
    """Raised when parsing encounters an error."""
    pass


class RuntimeErrorLyric(Exception):
    """Raised when runtime execution encounters an error."""
    pass
