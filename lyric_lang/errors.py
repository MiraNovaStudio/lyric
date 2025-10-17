"""
Error classes for the Lyric language.
Defines custom exceptions for different phases of execution.
"""

from typing import List, Optional, Dict, Any


class StackFrame:
    """Represents a single frame in the call stack."""
    
    def __init__(self, function_name: str, filename: str, line: int, col: int = None, 
                 local_vars: Dict[str, Any] = None):
        self.function_name = function_name
        self.filename = filename
        self.line = line
        self.col = col
        self.local_vars = local_vars or {}
    
    def __repr__(self):
        if self.col is not None:
            return f"{self.function_name} at {self.filename}:{self.line}:{self.col}"
        else:
            return f"{self.function_name} at {self.filename}:{self.line}"


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

    def __init__(self, message: str, line: int = None, col: int = None, filename: str = None,
                 stack_trace: List[StackFrame] = None):
        self.message = message
        self.line = line
        self.col = col
        self.filename = filename
        self.stack_trace = stack_trace or []

        # Format error message with location information
        if filename and line is not None:
            if col is not None:
                super().__init__(f"Runtime Error in '{filename}' [line {line}, col {col}]: "
                                 f"{message}")
            else:
                super().__init__(f"Runtime Error in '{filename}' [line {line}]: {message}")
        else:
            super().__init__(f"Runtime Error: {message}")
    
    def format_stack_trace(self) -> str:
        """Format the stack trace as a readable string."""
        if not self.stack_trace:
            return ""
        
        lines = ["Stack trace:"]
        for i, frame in enumerate(self.stack_trace):
            lines.append(f"  {i + 1}. {frame}")
        
        return "\n".join(lines)
    
    def format_debug_info(self) -> str:
        """Format debug information including stack trace and variables."""
        if not self.stack_trace:
            return ""
        
        lines = ["Debug information:"]
        lines.append(self.format_stack_trace())
        
        # Add variable information for each frame
        for i, frame in enumerate(self.stack_trace):
            if frame.local_vars:
                lines.append(f"\nFrame {i + 1} variables:")
                for var_name, var_value in frame.local_vars.items():
                    lines.append(f"  {var_name} = {var_value}")
        
        return "\n".join(lines)


class NameErrorLyric(RuntimeErrorLyric):
    """Exception raised when an undefined variable or function is referenced."""
    pass
