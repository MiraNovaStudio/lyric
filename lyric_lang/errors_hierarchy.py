"""
Built-in error hierarchy for the Lyric language.
Provides Error, TypeError, ValueError, NameError, and RuntimeError classes.
"""

from lyric_lang.errors import RuntimeErrorLyric


class Error:
    """Base error class for all Lyric exceptions."""
    
    def __init__(self, message: str = ""):
        self.message = message
        self.error_type = "Error"
    
    def __str__(self):
        return f"{self.error_type}: {self.message}"
    
    def raise_error(self, line: int = None, col: int = None, filename: str = None):
        """Raise this error as a RuntimeErrorLyric."""
        return RuntimeErrorLyric(
            message=str(self),
            line=line,
            col=col,
            filename=filename
        )


class TypeError(Error):
    """Error raised when an operation or function is applied to an object of inappropriate type."""
    
    def __init__(self, message: str = ""):
        super().__init__(message)
        self.error_type = "TypeError"


class ValueError(Error):
    """Error raised when a function receives an argument of correct type but inappropriate value."""
    
    def __init__(self, message: str = ""):
        super().__init__(message)
        self.error_type = "ValueError"


class NameError(Error):
    """Error raised when a local or global name is not found."""
    
    def __init__(self, message: str = ""):
        super().__init__(message)
        self.error_type = "NameError"


class RuntimeError(Error):
    """Error raised when an error does not belong to any other category."""
    
    def __init__(self, message: str = ""):
        super().__init__(message)
        self.error_type = "RuntimeError"


# Factory function to create error instances
def create_error(error_type: str, message: str = "") -> Error:
    """Create an error instance based on the error type name."""
    if error_type == "Error":
        return Error(message)
    elif error_type == "TypeError":
        return TypeError(message)
    elif error_type == "ValueError":
        return ValueError(message)
    elif error_type == "NameError":
        return NameError(message)
    elif error_type == "RuntimeError":
        return RuntimeError(message)
    else:
        # Unknown error type, default to RuntimeError
        return RuntimeError(f"Unknown error type '{error_type}': {message}")


# Export all error classes
__all__ = ['Error', 'TypeError', 'ValueError', 'NameError', 'RuntimeError', 'create_error']
