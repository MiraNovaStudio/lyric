# Lyric Programming Language
# Copyright (c) 2025 MiraNova Studios
# Developed by Michael (Aeonath), ChatGPT, and Claude
# Licensed under the MIT License with Source Attribution

"""Runtime module with built-in functions."""

from typing import Any, Iterator
from lyric.errors import RuntimeErrorLyric


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


def isinstance_builtin(obj: Any, class_or_type: Any) -> bool:
    """Built-in isinstance function for checking type names."""
    # Handle Lyric class instances
    if isinstance(obj, dict) and '__instance_class__' in obj:
        instance_class = obj['__instance_class__']
        
        # Check against class definition (dict)
        if isinstance(class_or_type, dict) and '__class_name__' in class_or_type:
            return instance_class == class_or_type['__class_name__']
        
        # Check against class name string
        if isinstance(class_or_type, str):
            return instance_class == class_or_type
    
    # Handle Python built-in types
    if isinstance(class_or_type, type):
        return isinstance(obj, class_or_type)
    
    # Handle string type names
    if isinstance(class_or_type, str):
        if class_or_type == "int":
            return isinstance(obj, int)
        elif class_or_type == "float":
            return isinstance(obj, float)
        elif class_or_type == "str":
            return isinstance(obj, str)
        elif class_or_type == "list":
            return isinstance(obj, list)
        elif class_or_type == "dict":
            return isinstance(obj, dict)
        elif class_or_type == "bool":
            return isinstance(obj, bool)
        elif class_or_type == "god":
            return isinstance(obj, bool)  # god type represents boolean values
        elif class_or_type == "bin":
            return isinstance(obj, bool)  # bin is an alias for god
        elif class_or_type == "None":
            return obj is None
        elif class_or_type == "pyobject":
            # pyobject represents any Python object that's not a basic Lyric type
            return not (isinstance(obj, dict) and '__instance_class__' in obj)
    
    # Handle when class_or_type is a built-in function (int_builtin, str_builtin, etc.)
    # Map built-in functions to their corresponding Python types
    if callable(class_or_type):
        if class_or_type.__name__ == "int_builtin":
            return isinstance(obj, int)
        elif class_or_type.__name__ == "float_builtin":
            return isinstance(obj, float)
        elif class_or_type.__name__ == "str_builtin":
            return isinstance(obj, str)
        elif class_or_type.__name__ == "list_builtin":
            return isinstance(obj, list)
        elif class_or_type.__name__ == "dict_builtin":
            return isinstance(obj, dict)
        elif class_or_type.__name__ == "bool_builtin":
            return isinstance(obj, bool)
    
    return False


def type_builtin(obj: Any) -> str:
    """Built-in type function returning the object's class name or Python type."""
    # Handle Lyric class instances
    if isinstance(obj, dict) and '__instance_class__' in obj:
        return obj['__instance_class__']
    
    # Handle Python built-in types (check bool first since it's a subclass of int)
    if isinstance(obj, bool):
        return "god"  # Return "god" for boolean types (honoring Kurt Gödel)
    elif isinstance(obj, int):
        return "int"
    elif isinstance(obj, float):
        return "float"
    elif isinstance(obj, str):
        return "str"
    elif isinstance(obj, list):
        return "list"
    elif obj is None:
        return "None"
    else:
        # For any other Python object, return "pyobject"
        return "pyobject"


def append_builtin(obj: Any, item: Any) -> None:
    """Built-in append function that adds an item to a list."""
    if isinstance(obj, list):
        obj.append(item)
    else:
        raise RuntimeErrorLyric(f"append() only works on lists, got {type(obj).__name__}")


def keys_builtin(obj: Any) -> list:
    """Built-in keys function that returns dictionary keys."""
    if isinstance(obj, dict):
        return list(obj.keys())
    else:
        raise RuntimeErrorLyric(f"keys() only works on dictionaries, got {type(obj).__name__}")


def values_builtin(obj: Any) -> list:
    """Built-in values function that returns dictionary values."""
    if isinstance(obj, dict):
        return list(obj.values())
    else:
        raise RuntimeErrorLyric(f"values() only works on dictionaries, got {type(obj).__name__}")


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
    env['isinstance'] = isinstance_builtin
    env['type'] = type_builtin
    env['append'] = append_builtin
    env['keys'] = keys_builtin
    env['values'] = values_builtin
