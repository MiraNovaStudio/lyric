"""
Lexer module for the Lyric language.
Tokenizes source code into tokens.
"""

import re
from dataclasses import dataclass
from typing import List, Optional
from lyric.errors import LexError


@dataclass
class Token:
    """Represents a token with type, value, and position information."""
    type: str
    value: str
    line: int
    col: int


class Lexer:
    """Lexical analyzer for the Lyric language."""

    # Keywords
    KEYWORDS = {
        'def', 'class', 'if', 'else', 'given', 'done', 'end',
        'try', 'except', 'finally', 'import', 'from', 'as', 'return',
        'true', 'false', 'and', 'or', 'not', 'in', 'None', 'raise'
    }

    # Token patterns
    TOKEN_PATTERNS = [
        ('CLASS_END', r'\+\+\+'),                    # Class terminator
        ('NEWLINE', r'\n'),                          # Newline
        ('WHITESPACE', r'[ \t]+'),                   # Whitespace (ignored)

        # Identifiers and keywords
        ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),

        # Numbers
        ('FLOAT', r'\d+\.\d+'),
        ('INTEGER', r'\d+'),

        # Strings (with escaped quotes support)
        ('STRING', r'"([^"\\]|\\.)*"'),

        # Operators
        ('EQ', r'=='),                               # Equality
        ('NE', r'!='),                               # Not equal
        ('LE', r'<='),                               # Less or equal
        ('GE', r'>='),                               # Greater or equal
        ('ASSIGN', r'='),                            # Assignment
        ('LT', r'<'),                                # Less than
        ('GT', r'>'),                                # Greater than
        ('PLUS', r'\+'),                             # Addition
        ('MINUS', r'-'),                             # Subtraction
        ('MULTIPLY', r'\*'),                         # Multiplication
        ('DIVIDE', r'/'),                            # Division
        ('MODULO', r'%'),                            # Modulo

        # Delimiters
        ('LPAREN', r'\('),                           # Left parenthesis
        ('RPAREN', r'\)'),                           # Right parenthesis
        ('LBRACE', r'\{'),                           # Left brace
        ('RBRACE', r'\}'),                           # Right brace
        ('LBRACKET', r'\['),                         # Left bracket (for lists)
        ('RBRACKET', r'\]'),                         # Right bracket (for lists)
        ('COLON', r':'),                             # Colon
        ('COMMA', r','),                             # Comma
        ('SEMICOLON', r';'),                         # Semicolon
        ('DOT', r'\.'),                              # Dot
    ]

    def __init__(self, source: str, filename: str = None):
        self.source = source
        self.filename = filename
        self.tokens = []
        self.line = 1
        self.col = 1
        self.pos = 0

    def tokenize(self) -> List[Token]:
        """Tokenize the source code and return a list of tokens."""
        self.tokens = []
        self.line = 1
        self.col = 1
        self.pos = 0

        while self.pos < len(self.source):
            self._skip_whitespace_and_comments()
            if self.pos >= len(self.source):
                break

            token = self._get_next_token()
            if token:
                self.tokens.append(token)

        return self.tokens

    def _skip_whitespace_and_comments(self):
        """Skip whitespace and comments."""
        while self.pos < len(self.source):
            # Skip whitespace
            if self.source[self.pos] in ' \t':
                self.pos += 1
                self.col += 1
            # Skip comments
            elif self.source[self.pos] == '#':
                # Skip to end of line
                while self.pos < len(self.source) and self.source[self.pos] != '\n':
                    self.pos += 1
                    self.col += 1
            else:
                break

    def _get_next_token(self) -> Optional[Token]:
        """Get the next token from the source."""
        remaining_source = self.source[self.pos:]

        for token_type, pattern in self.TOKEN_PATTERNS:
            match = re.match(pattern, remaining_source)
            if match:
                value = match.group(0)
                token = Token(token_type, value, self.line, self.col)

                # Update position
                if token_type == 'NEWLINE':
                    self.line += 1
                    self.col = 1
                else:
                    self.col += len(value)
                self.pos += len(value)

                # Convert identifier to keyword if it matches
                if token_type == 'IDENTIFIER' and value in self.KEYWORDS:
                    token.type = value.upper()

                return token

        # If no pattern matches, it's an error
        raise LexError(f"Unexpected character '{self.source[self.pos]}'",
                       line=self.line, col=self.col, filename=self.filename)


def tokenize(source: str, filename: str = None) -> List[Token]:
    """Tokenize source code and return a list of tokens.

    Args:
        source: The source code to tokenize
        filename: Optional filename for error reporting

    Returns:
        List of Token objects
    """
    lexer = Lexer(source, filename)
    return lexer.tokenize()
