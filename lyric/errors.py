"""
Error classes for the Lyric language.
Defines custom exceptions for different phases of execution.
"""


class LexError(Exception):
    """Exception raised during lexing/tokenization."""
    pass


class ParseError(Exception):
    """Exception raised during parsing."""
    pass


class RuntimeErrorLyric(Exception):
    """Exception raised during runtime execution."""
    pass
