"""Lexer module for tokenizing Lyric source code."""

from dataclasses import dataclass
from typing import List
from lyric.errors import LexError


@dataclass
class Token:
    """Represents a token with type, value, line, and column information."""
    type: str
    value: str
    line: int
    col: int


class Lexer:
    """Tokenizes Lyric source code into a list of tokens."""
    
    # Keywords
    KEYWORDS = {
        'def', 'class', 'if', 'else', 'given', 'for', 'done', 'end', 
        'try', 'catch', 'finally', 'fade', 'and', 'or', 'not', 'in', 'as', 'return',
        'int', 'str', 'flt', 'var', 'pyobject', 'rex', 'god', 'bin', 'True', 'False', 'true', 'false', 'None', 'raise', 'importpy'
    }
    
    # Single character operators and delimiters
    SINGLE_CHARS = {
        '+', '-', '*', '/', '=', '(', ')', '{', '}', ':', ',', ';', '.', '[', ']'
    }
    
    # Operator type mappings
    OPERATOR_TYPES = {
        '>': 'GT',
        '<': 'LT',
        '=': 'ASSIGN',
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'MULTIPLY',
        '/': 'DIVIDE',
        '(': 'LPAREN',
        ')': 'RPAREN',
        '{': 'LBRACE',
        '}': 'RBRACE',
        ':': 'COLON',
        ',': 'COMMA',
        ';': 'SEMICOLON',
        '.': 'DOT',
        '[': 'LBRACKET',
        ']': 'RBRACKET'
    }
    
    # Multi-character operators
    MULTI_CHARS = {
        '==', '!=', '<', '<=', '>', '>=', '+++'
    }
    
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.current = 0
        self.line = 1
        self.col = 1
        self.start_col = 1
    
    def tokenize(self) -> List[Token]:
        """Tokenize the source code and return a list of tokens."""
        self.tokens = []
        self.current = 0
        self.line = 1
        self.col = 1
        
        while not self._is_at_end():
            self.start_col = self.col
            self._scan_token()
        
        # Add EOF token
        self.tokens.append(Token('EOF', '', self.line, self.col))
        return self.tokens
    
    def _is_at_end(self) -> bool:
        """Check if we've reached the end of the source."""
        return self.current >= len(self.source)
    
    def _advance(self) -> str:
        """Advance to the next character and return the previous one."""
        if not self._is_at_end():
            char = self.source[self.current]
            self.current += 1
            if char == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            return char
        return ''
    
    def _peek(self) -> str:
        """Look at the current character without advancing."""
        if self._is_at_end():
            return ''
        return self.source[self.current]
    
    def _peek_next(self) -> str:
        """Look at the next character without advancing."""
        if self.current + 1 >= len(self.source):
            return ''
        return self.source[self.current + 1]
    
    def _scan_token(self):
        """Scan the next token."""
        char = self._advance()
        
        # Skip whitespace
        if char in ' \t\r':
            return
        
        # Handle newlines
        if char == '\n':
            self.tokens.append(Token('NEWLINE', '\n', self.line - 1, self.start_col))
            return
        
        # Handle comments
        if char == '#':
            self._scan_comment()
            return
        
        # Handle strings
        if char == '"':
            self._scan_string()
            return
        
        # Handle regex literals
        if char == '/':
            # Check if this is a regex literal or division
            # Regex literals must be followed by a non-whitespace character
            # and must have a closing slash
            if not self._is_at_end() and self._peek() != ' ' and self._peek() != '\t' and self._peek() != '\n':
                # Look ahead to see if there's a closing slash
                temp_pos = self.current
                has_closing_slash = False
                while temp_pos < len(self.source) and self.source[temp_pos] != '\n':
                    if self.source[temp_pos] == '/':
                        has_closing_slash = True
                        break
                    temp_pos += 1
                
                if has_closing_slash:
                    self._scan_regex()
                    return
            
            # If not a regex literal, treat as division
            self.tokens.append(Token('DIVIDE', char, self.line, self.start_col))
            return
        
        # Handle numbers
        if char.isdigit():
            self._scan_number(char)
            return
        
        # Handle identifiers and keywords
        if char.isalpha() or char == '_':
            self._scan_identifier(char)
            return
        
        # Handle multi-character operators
        if char in '<>=!+':
            self._scan_multi_char_operator(char)
            return
        
        # Handle single character operators and delimiters
        if char in self.SINGLE_CHARS:
            token_type = self.OPERATOR_TYPES.get(char, char)
            self.tokens.append(Token(token_type, char, self.line, self.start_col))
            return
        
        # Unknown character
        raise LexError(f"Unexpected character '{char}' at line {self.line}, column {self.start_col}")
    
    def _scan_comment(self):
        """Scan a comment until end of line."""
        while self._peek() != '\n' and not self._is_at_end():
            self._advance()
    
    def _scan_string(self):
        """Scan a string literal."""
        start_line = self.line
        start_col = self.start_col
        value = ''
        
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == '\n':
                raise LexError(f"Unterminated string at line {start_line}, column {start_col}")
            value += self._advance()
        
        if self._is_at_end():
            raise LexError(f"Unterminated string at line {start_line}, column {start_col}")
        
        # Consume the closing quote
        self._advance()
        
        self.tokens.append(Token('STRING', value, start_line, start_col))
    
    def _scan_regex(self):
        """Scan a regex literal."""
        start_line = self.line
        start_col = self.start_col
        value = ''
        
        while self._peek() != '/' and not self._is_at_end():
            if self._peek() == '\n':
                raise LexError(f"Unterminated regex at line {start_line}, column {start_col}")
            value += self._advance()
        
        if self._is_at_end():
            raise LexError(f"Unterminated regex at line {start_line}, column {start_col}")
        
        # Consume the closing slash
        self._advance()
        
        # Validate regex pattern
        try:
            import re
            re.compile(value)
        except re.error as e:
            raise LexError(f"Invalid regex pattern '{value}' at line {start_line}, column {start_col}: {e}")
        
        self.tokens.append(Token('REGEX_LITERAL', value, start_line, start_col))
    
    def _scan_number(self, first_char: str):
        """Scan a number (integer or float)."""
        start_line = self.line
        start_col = self.start_col
        value = first_char
        
        # Scan integer part
        while self._peek().isdigit():
            value += self._advance()
        
        # Check for decimal point
        if self._peek() == '.' and self._peek_next().isdigit():
            value += self._advance()  # consume the '.'
            while self._peek().isdigit():
                value += self._advance()
            self.tokens.append(Token('FLOAT', float(value), start_line, start_col))
        else:
            self.tokens.append(Token('INT', int(value), start_line, start_col))
    
    def _scan_identifier(self, first_char: str):
        """Scan an identifier or keyword."""
        start_line = self.line
        start_col = self.start_col
        value = first_char
        
        while self._peek().isalnum() or self._peek() == '_':
            value += self._advance()
        
        # Check if it's a keyword
        if value in self.KEYWORDS:
            if value in ('True', 'False', 'true', 'false'):
                # Convert boolean keywords to actual boolean values
                bool_value = value in ('True', 'true')
                self.tokens.append(Token('BOOLEAN', bool_value, start_line, start_col))
            elif value == 'None':
                # Convert None keyword to actual None value
                self.tokens.append(Token('NONE', None, start_line, start_col))
            elif value in ('int', 'str', 'flt', 'var', 'pyobject', 'rex', 'god', 'bin'):
                # Type keywords can also be used as identifiers in expressions
                # We'll let the parser decide based on context
                self.tokens.append(Token('TYPE_OR_IDENT', value, start_line, start_col))
            elif value == 'for':
                # Map 'for' to 'GIVEN' token for syntactic sugar
                self.tokens.append(Token('GIVEN', 'for', start_line, start_col))
            else:
                self.tokens.append(Token(value.upper(), value, start_line, start_col))
        else:
            self.tokens.append(Token('IDENT', value, start_line, start_col))
    
    def _scan_multi_char_operator(self, first_char: str):
        """Scan multi-character operators."""
        start_line = self.line
        start_col = self.start_col
        
        if first_char == '+' and self._peek() == '+' and self._peek_next() == '+':
            # Handle +++ (CLASS_END)
            self._advance()  # consume second +
            self._advance()  # consume third +
            self.tokens.append(Token('CLASS_END', '+++', start_line, start_col))
        elif first_char in '<>=!' and self._peek() == '=':
            # Handle <=, >=, ==, !=
            operator = first_char + self._advance()
            self.tokens.append(Token(operator, operator, start_line, start_col))
        else:
            # Single character operator - use proper type
            token_type = self.OPERATOR_TYPES.get(first_char, first_char)
            self.tokens.append(Token(token_type, first_char, start_line, start_col))


def tokenize(source: str) -> List[Token]:
    """Tokenize source code and return a list of tokens."""
    lexer = Lexer(source)
    return lexer.tokenize()