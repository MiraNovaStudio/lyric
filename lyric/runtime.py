"""Runtime module with built-in functions."""

import sys
from typing import Any, List, Union, Iterator


def print_builtin(*args: Any) -> None:
    """Built-in print function that writes to stdout with single space joining."""
    if not args:
        print()
        return
    
    # Convert all arguments to strings and join with single space
    output = ' '.join(str(arg) for arg in args)
    print(output)


def input_builtin(prompt: str = "") -> str:
    """Built-in input function that reads from stdin."""
    return input(prompt)


def int_builtin(value: Any) -> int:
    """Built-in int conversion function."""
    return int(value)


def float_builtin(value: Any) -> float:
    """Built-in float conversion function."""
    return float(value)


def str_builtin(value: Any) -> str:
    """Built-in str conversion function."""
    return str(value)


def range_builtin(n: int) -> Iterator[int]:
    """Built-in range function that yields 0..N-1."""
    return range(n)


def len_builtin(obj: Any) -> int:
    """Built-in len function."""
    return len(obj)


def open_builtin(path: str) -> Iterator[str]:
    """Built-in open function that returns an iterable over lines."""
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.rstrip('\n\r')


def register_builtins(env: dict) -> None:
    """Register all built-in functions in the given environment."""
    env['print'] = print_builtin
    env['input'] = input_builtin
    env['int'] = int_builtin
    env['float'] = float_builtin
    env['str'] = str_builtin
    env['range'] = range_builtin
    env['len'] = len_builtin
    env['open'] = open_builtin
