"""Error classes for Lyric language."""

class LexError(Exception):
    """Raised when lexing fails."""
    def __init__(self, message: str, line: int = 0, column: int = 0, filename: str = ""):
        super().__init__(message)
        self.line = line
        self.column = column
        self.filename = filename
    
    def __str__(self):
        if self.filename:
            return f"Lexical error in {self.filename} at line {self.line}, column {self.column}: {super().__str__()}"
        else:
            return f"Lexical error at line {self.line}, column {self.column}: {super().__str__()}"


class ParseError(Exception):
    """Raised when parsing fails."""
    def __init__(self, message: str, line: int = 0, column: int = 0, filename: str = ""):
        super().__init__(message)
        self.line = line
        self.column = column
        self.filename = filename
    
    def __str__(self):
        if self.filename:
            return f"Parse error in {self.filename} at line {self.line}, column {self.column}: {super().__str__()}"
        else:
            return f"Parse error at line {self.line}, column {self.column}: {super().__str__()}"


class SyntaxErrorLyric(ParseError):
    """Raised when syntax is invalid."""
    pass


class RuntimeErrorLyric(Exception):
    """Raised when runtime execution fails."""
    def __init__(self, message: str, line: int = 0, column: int = 0, filename: str = ""):
        super().__init__(message)
        self.line = line
        self.column = column
        self.filename = filename
    
    def __str__(self):
        if self.filename:
            return f"Runtime error in {self.filename} at line {self.line}, column {self.column}: {super().__str__()}"
        else:
            return f"Runtime error at line {self.line}, column {self.column}: {super().__str__()}"


class NameErrorLyric(RuntimeErrorLyric):
    """Raised when a name is not defined."""
    pass
