"""
Runtime module for the Lyric language.
Provides built-in functions and runtime support.
"""

import sys
from typing import Any, List, Optional, Union
from lyric.errors import RuntimeErrorLyric


class BuiltinFunction:
    """Represents a built-in function."""
    
    def __init__(self, name: str, func: callable, arity: Optional[int] = None):
        self.name = name
        self.func = func
        self.arity = arity  # None means variable arguments
    
    def call(self, args: List[Any]) -> Any:
        """Call the built-in function with arguments."""
        if self.arity is not None and len(args) != self.arity:
            raise RuntimeErrorLyric(f"{self.name}() takes {self.arity} argument(s), got {len(args)}")
        return self.func(args)


def _builtin_print(args: List[Any]) -> None:
    """Built-in print function."""
    # Convert all arguments to strings and join with spaces
    values = []
    for arg in args:
        values.append(str(arg))
    
    print(' '.join(values))


def _builtin_input(args: List[Any]) -> str:
    """Built-in input function."""
    if len(args) == 0:
        prompt = ""
    elif len(args) == 1:
        prompt = str(args[0])
    else:
        raise RuntimeErrorLyric(f"input() takes 0-1 arguments, got {len(args)}")
    
    return input(prompt)


def _builtin_int(args: List[Any]) -> int:
    """Built-in int conversion function."""
    if len(args) != 1:
        raise RuntimeErrorLyric(f"int() takes 1 argument, got {len(args)}")
    
    try:
        return int(args[0])
    except (ValueError, TypeError) as e:
        raise RuntimeErrorLyric(f"int() conversion failed: {e}")


def _builtin_float(args: List[Any]) -> float:
    """Built-in float conversion function."""
    if len(args) != 1:
        raise RuntimeErrorLyric(f"float() takes 1 argument, got {len(args)}")
    
    try:
        return float(args[0])
    except (ValueError, TypeError) as e:
        raise RuntimeErrorLyric(f"float() conversion failed: {e}")


def _builtin_str(args: List[Any]) -> str:
    """Built-in string conversion function."""
    if len(args) != 1:
        raise RuntimeErrorLyric(f"str() takes 1 argument, got {len(args)}")
    
    return str(args[0])


def _builtin_range(args: List[Any]) -> List[int]:
    """Built-in range function."""
    if len(args) == 1:
        # range(stop)
        stop = int(args[0])
        return list(range(stop))
    elif len(args) == 2:
        # range(start, stop)
        start = int(args[0])
        stop = int(args[1])
        return list(range(start, stop))
    elif len(args) == 3:
        # range(start, stop, step)
        start = int(args[0])
        stop = int(args[1])
        step = int(args[2])
        return list(range(start, stop, step))
    else:
        raise RuntimeErrorLyric(f"range() takes 1-3 arguments, got {len(args)}")


def _builtin_len(args: List[Any]) -> int:
    """Built-in len function."""
    if len(args) != 1:
        raise RuntimeErrorLyric(f"len() takes 1 argument, got {len(args)}")
    
    try:
        return len(args[0])
    except TypeError as e:
        raise RuntimeErrorLyric(f"len() failed: {e}")


class FileWrapper:
    """Wrapper for file objects to make them iterable over lines."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file = None
    
    def __iter__(self):
        """Make the file iterable over lines."""
        try:
            self.file = open(self.file_path, 'r', encoding='utf-8')
            return self
        except FileNotFoundError:
            raise RuntimeErrorLyric(f"File not found: {self.file_path}")
        except Exception as e:
            raise RuntimeErrorLyric(f"Error opening file {self.file_path}: {e}")
    
    def __next__(self):
        """Get the next line from the file."""
        if self.file is None:
            raise RuntimeErrorLyric("File not opened")
        
        line = self.file.readline()
        if line == "":
            self.file.close()
            raise StopIteration
        
        return line.rstrip('\n\r')  # Remove line endings


def _builtin_open(args: List[Any]) -> FileWrapper:
    """Built-in open function."""
    if len(args) != 1:
        raise RuntimeErrorLyric(f"open() takes 1 argument, got {len(args)}")
    
    file_path = str(args[0])
    return FileWrapper(file_path)


def register_builtins(env: dict) -> None:
    """Register all built-in functions in the given environment.
    
    Args:
        env: Dictionary to populate with built-in functions
    """
    builtins = [
        BuiltinFunction("print", _builtin_print),  # Variable arguments
        BuiltinFunction("input", _builtin_input),  # 0-1 arguments
        BuiltinFunction("int", _builtin_int, 1),
        BuiltinFunction("float", _builtin_float, 1),
        BuiltinFunction("str", _builtin_str, 1),
        BuiltinFunction("range", _builtin_range),  # Variable arguments (1-3)
        BuiltinFunction("len", _builtin_len, 1),
        BuiltinFunction("open", _builtin_open, 1),
    ]
    
    for builtin in builtins:
        env[builtin.name] = builtin


# For testing purposes, we can inject custom input functions
_input_injection = None

def set_input_injection(func: callable) -> None:
    """Set a custom input function for testing.
    
    Args:
        func: Function that takes no arguments and returns a string
    """
    global _input_injection
    _input_injection = func


def get_input_injection() -> Optional[callable]:
    """Get the current input injection function.
    
    Returns:
        The input injection function or None
    """
    return _input_injection
