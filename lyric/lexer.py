"""
Lyric Language Lexer
Converts source code into tokens for parsing.
"""

import re
from lyric.errors import LexError


class Token:
    """Represents a token in the Lyric language."""
    
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, {self.line}, {self.column})"


class Lexer:
    """Lexical analyzer for the Lyric language."""
    
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        # Keywords (must come before IDENTIFIER)
        self.keywords = {
            'def': 'DEF',
            'class': 'CLASS',
            'if': 'IF',
            'else': 'ELSE',
            'given': 'GIVEN',
            'done': 'DONE',
            'end': 'END',
            'try': 'TRY',
            'except': 'EXCEPT',
            'finally': 'FINALLY',
            'in': 'IN',
            'and': 'AND',
            'or': 'OR',
            'not': 'NOT',
        }
        
        # Token patterns
        self.patterns = [
            ('NUMBER', r'\d+(\.\d*)?'),
            ('STRING', r'"[^"]*"'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('ASSIGN', r'='),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('MULTIPLY', r'\*'),
            ('DIVIDE', r'/'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('LBRACKET', r'\['),
            ('RBRACKET', r'\]'),
            ('COMMA', r','),
            ('COLON', r':'),
            ('SEMICOLON', r';'),
            ('DOT', r'\.'),
            ('EQUAL', r'=='),
            ('NOTEQUAL', r'!='),
            ('LESS', r'<'),
            ('LESSEQUAL', r'<='),
            ('GREATER', r'>'),
            ('GREATEREQUAL', r'>='),
            ('WHITESPACE', r'\s+'),
            ('COMMENT', r'#.*(?:\n|$)'),
        ]
        
        # Compile patterns
        self.compiled_patterns = [(name, re.compile(pattern)) for name, pattern in self.patterns]
    
    def tokenize(self):
        """Tokenize the input text."""
        while self.pos < len(self.text):
            self._skip_whitespace()
            if self.pos >= len(self.text):
                break
                
            matched = False
            for token_type, pattern in self.compiled_patterns:
                match = pattern.match(self.text, self.pos)
                if match:
                    value = match.group(0)
                    
                    # Skip whitespace and comments
                    if token_type in ('WHITESPACE', 'COMMENT'):
                        self._advance(len(value))
                        continue
                    
                    # Check if identifier is a keyword
                    if token_type == 'IDENTIFIER' and value in self.keywords:
                        token_type = self.keywords[value]
                    
                    # Create token
                    token = Token(token_type, value, self.line, self.column)
                    self.tokens.append(token)
                    self._advance(len(value))
                    matched = True
                    break
            
            if not matched:
                raise LexError(f"Unexpected character '{self.text[self.pos]}' at line {self.line}, column {self.column}")
        
        # Add EOF token
        self.tokens.append(Token('EOF', None, self.line, self.column))
        return self.tokens
    
    def _skip_whitespace(self):
        """Skip whitespace characters."""
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            if self.text[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def _advance(self, length):
        """Advance position by given length."""
        for i in range(length):
            if self.text[self.pos + i] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
        self.pos += length
