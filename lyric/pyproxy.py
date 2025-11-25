# Lyric Programming Language
# Copyright (c) 2025 MiraNova Studios
# Designed and Architected by Michael (Aeonath) and ChatGPT
# Implemented by Claude
# Licensed under the GNU General Public License v3.0

"""Python module proxy for importpy functionality."""

from typing import Any
from lyric.errors import RuntimeErrorLyric


class PyModuleProxy:
    """Proxy object that forwards attribute access to Python modules."""
    
    def __init__(self, module_name: str):
        """Initialize the proxy with a Python module name."""
        self._module_name = module_name
        try:
            self._module = __import__(module_name)
        except ImportError as e:
            raise RuntimeErrorLyric(f"ImportError: cannot import Python module '{module_name}'")
    
    def __getattr__(self, name: str) -> Any:
        """Forward attribute access to the underlying Python module."""
        try:
            attr = getattr(self._module, name)
            # Only wrap functions, not classes
            if callable(attr) and not isinstance(attr, type):
                return PyCallableProxy(attr, f"{self._module_name}.{name}")
            return attr
        except AttributeError as e:
            raise RuntimeErrorLyric(f"AttributeError: '{self._module_name}' has no attribute '{name}'")
    
    def __repr__(self) -> str:
        """Return a string representation of the proxy."""
        return f"<PyModuleProxy {self._module_name}>"


class PyCallableProxy:
    """Proxy for callable Python objects."""
    
    def __init__(self, callable_obj: Any, name: str):
        """Initialize the proxy with a callable object."""
        self._callable = callable_obj
        self._name = name
    
    def __call__(self, *args, **kwargs) -> Any:
        """Call the underlying callable object."""
        try:
            return self._callable(*args, **kwargs)
        except Exception as e:
            raise RuntimeErrorLyric(f"Error calling '{self._name}': {str(e)}")
    
    def __repr__(self) -> str:
        """Return a string representation of the proxy."""
        return f"<PyCallableProxy {self._name}>"
