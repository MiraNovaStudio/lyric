"""
Error classes for the Lyric language.
Defines custom exceptions for different phases of execution.
"""


class LexError(Exception):
    """Exception raised during lexing/tokenization."""
    
    def __init__(self, message: str, line: int = None, col: int = None, filename: str = None):
        self.message = message
        self.line = line
        self.col = col
        self.filename = filename
        
        # Format error message with location information
        if filename and line is not None:
            if col is not None:
                super().__init__(f"Lex Error in '{filename}' [line {line}, col {col}]: {message}")
            else:
                super().__init__(f"Lex Error in '{filename}' [line {line}]: {message}")
        else:
            super().__init__(f"Lex Error: {message}")


class ParseError(Exception):
    """Exception raised during parsing."""
    
    def __init__(self, message: str, line: int = None, col: int = None, filename: str = None):
        self.message = message
        self.line = line
        self.col = col
        self.filename = filename
        
        # Format error message with location information
        if filename and line is not None:
            if col is not None:
                super().__init__(f"Parse Error in '{filename}' [line {line}, col {col}]: {message}")
            else:
                super().__init__(f"Parse Error in '{filename}' [line {line}]: {message}")
        else:
            super().__init__(f"Parse Error: {message}")


class SyntaxErrorLyric(ParseError):
    """Exception raised for syntax errors during parsing."""
    pass


class RuntimeErrorLyric(Exception):
    """Exception raised during runtime execution."""
    
    def __init__(self, message: str, line: int = None, col: int = None, filename: str = None):
        self.message = message
        self.line = line
        self.col = col
        self.filename = filename
        
        # Format error message with location information
        if filename and line is not None:
            if col is not None:
                super().__init__(f"Runtime Error in '{filename}' [line {line}, col {col}]: {message}")
            else:
                super().__init__(f"Runtime Error in '{filename}' [line {line}]: {message}")
        else:
            super().__init__(f"Runtime Error: {message}")


class NameErrorLyric(RuntimeErrorLyric):
    """Exception raised when an undefined variable or function is referenced."""
    pass
