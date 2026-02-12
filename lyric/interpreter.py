# Lyric Programming Language
# Copyright (c) 2025 MiraNova Studios
# Designed and Architected by Michael (Aeonath) and ChatGPT
# Implemented by Claude
# Licensed under the GNU General Public License v3.0

"""Interpreter module for executing Lyric AST nodes."""

from typing import Any, List
import re
from lyric.ast_nodes import (
    ProgramNode, FunctionNode, IfNode, LoopNode, AssignNode, CallNode,
    BinaryOpNode, UnaryOpNode, LiteralNode, IdentifierNode, ClassNode, ReturnNode, BreakNode, ContinueNode,
    ListLiteralNode, DictLiteralNode, IndexNode, SliceNode, TypeDeclarationNode, MultiDeclarationNode, TryNode, CatchClauseNode, RaiseNode, ImportNode, ImportPyNode, RexNode, FileOpNode
)
from lyric.errors import (
    RuntimeErrorLyric, CompileErrorLyric, NameErrorLyric, EXCEPTION_TYPES,
    IndexErrorLyric, KeyErrorLyric, TypeErrorLyric, ValueErrorLyric,
    AttributeErrorLyric, ZeroDivisionErrorLyric, BreakSignal, ContinueSignal
)
from lyric.runtime import register_builtins


class RexMatch:
    """Represents a regex match result."""
    
    def __init__(self, match):
        self.match = match
    
    def group(self, index: int = 0) -> str:
        """Get the matched group by index."""
        if not isinstance(index, int):
            raise RuntimeErrorLyric(f"Type error: group() expects an integer index, but got {type(index).__name__}")
        try:
            return self.match.group(index)
        except IndexError:
            raise RuntimeErrorLyric(f"Index error: group {index} does not exist in this match")
    
    def __repr__(self):
        return f"RexMatch(match='{self.match.group(0)}')"


class RexObject:
    """Represents a compiled regex object with methods."""
    
    def __init__(self, compiled_pattern):
        self.pattern = compiled_pattern
    
    def match(self, text: str) -> bool:
        """Check if the regex matches the beginning of the text."""
        if not isinstance(text, str):
            raise RuntimeErrorLyric(f"Type error: rex.match() expects a string, but got {type(text).__name__}")
        return bool(self.pattern.match(text))
    
    def replace(self, source: str, replacement: str) -> str:
        """Replace all matches of the regex in the source string."""
        if not isinstance(source, str):
            raise RuntimeErrorLyric(f"Type error: rex.replace() expects a string as source, but got {type(source).__name__}")
        if not isinstance(replacement, str):
            raise RuntimeErrorLyric(f"Type error: rex.replace() expects a string as replacement, but got {type(replacement).__name__}")
        return self.pattern.sub(replacement, source)
    
    def search(self, text: str) -> 'RexMatch':
        """Search for the regex pattern anywhere in the text and return a match object."""
        if not isinstance(text, str):
            raise RuntimeErrorLyric(f"Type error: rex.search() expects a string, but got {type(text).__name__}")
        match = self.pattern.search(text)
        if match:
            return RexMatch(match)
        return None
    
    def findall(self, text: str) -> list:
        """Find all non-overlapping matches of the regex in the text."""
        if not isinstance(text, str):
            raise RuntimeErrorLyric(f"Type error: rex.findall() expects a string, but got {type(text).__name__}")
        return self.pattern.findall(text)
    
    def __repr__(self):
        return f"RexObject(pattern='{self.pattern.pattern}')"


class ArrObject:
    """Represents an arr (list) object with methods."""
    
    def __init__(self, elements: list = None):
        """Initialize ArrObject with a list of elements."""
        self.elements = elements if elements is not None else []
    
    def append(self, element: Any) -> None:
        """Add a single element to the end of the list."""
        self.elements.append(element)
    
    def clear(self) -> None:
        """Remove all elements, making the list empty."""
        self.elements.clear()
    
    def copy(self) -> 'ArrObject':
        """Return a shallow copy of the list."""
        return ArrObject(self.elements.copy())
    
    def count(self, value: Any) -> int:
        """Return number of occurrences of value."""
        return self.elements.count(value)
    
    def index(self, value: Any, start: int = 0, end: int = None) -> int:
        """Return index of first occurrence; raise ValueError if not found."""
        try:
            if end is None:
                return self.elements.index(value, start)
            else:
                return self.elements.index(value, start, end)
        except ValueError:
            raise ValueErrorLyric(f"'{value}' is not in arr")
    
    def insert(self, index: int, element: Any) -> None:
        """Insert element at index, shifting items right."""
        if not isinstance(index, int):
            raise TypeErrorLyric(f"insert() expects an integer index, but got {type(index).__name__}")
        self.elements.insert(index, element)
    
    def pop(self, index: int = -1) -> Any:
        """Remove and return item at index; default to last item; raise IndexError if invalid."""
        if not isinstance(index, int):
            raise TypeErrorLyric(f"pop() expects an integer index, but got {type(index).__name__}")
        if not self.elements:
            raise IndexErrorLyric("pop from empty arr")
        try:
            return self.elements.pop(index)
        except IndexError:
            raise IndexErrorLyric(f"pop index out of range")
    
    def remove(self, value: Any) -> None:
        """Remove first occurrence of value; raise ValueError if missing."""
        try:
            self.elements.remove(value)
        except ValueError:
            raise ValueErrorLyric(f"arr.remove(x): x not in arr")
    
    def reverse(self) -> None:
        """Reverse list in place."""
        self.elements.reverse()
    
    def sort(self, key=None, reverse=None) -> None:
        """Sort list in place; support optional key and reverse parameters."""
        try:
            # Handle reverse parameter - defaults to False
            reverse_val = False if reverse is None else reverse
            
            if key is None or key is False:
                # No key function, just sort normally
                self.elements.sort(reverse=reverse_val)
            else:
                # key would be a callable if provided
                if callable(key):
                    self.elements.sort(key=key, reverse=reverse_val)
                else:
                    raise TypeErrorLyric(f"sort() key parameter must be callable, got {type(key).__name__}")
        except TypeError as e:
            raise TypeErrorLyric(f"sort() error: {e}")
    
    def len(self) -> int:
        """Return number of elements in the list."""
        return len(self.elements)
    
    def max(self) -> Any:
        """Return largest element; error if list is empty."""
        if not self.elements:
            raise ValueErrorLyric("max() arg is an empty arr")
        try:
            return max(self.elements)
        except TypeError as e:
            raise TypeErrorLyric(f"max() error: {e}")
    
    def min(self) -> Any:
        """Return smallest element; error if list is empty."""
        if not self.elements:
            raise ValueErrorLyric("min() arg is an empty arr")
        try:
            return min(self.elements)
        except TypeError as e:
            raise TypeErrorLyric(f"min() error: {e}")
    
    def sum(self) -> Any:
        """Return sum of numeric elements; raise TypeError on non-numeric values."""
        if not self.elements:
            return 0
        try:
            return sum(self.elements)
        except TypeError:
            # Check which element is non-numeric
            for i, elem in enumerate(self.elements):
                if not isinstance(elem, (int, float)):
                    raise TypeErrorLyric(f"sum() does not support non-numeric types: element at index {i} is {type(elem).__name__}")
            # If we get here, re-raise the original error
            raise TypeErrorLyric(f"sum() error with arr elements")
    
    def __repr__(self):
        return str(self.elements)
    
    def __str__(self):
        return str(self.elements)
    
    def __len__(self):
        return len(self.elements)
    
    def __getitem__(self, key):
        """Support indexing and slicing."""
        if isinstance(key, slice):
            # Return a new ArrObject with the sliced elements
            return ArrObject(self.elements[key])
        else:
            # Return the element directly (not wrapped in ArrObject)
            return self.elements[key]
    
    def __setitem__(self, key, value):
        """Support item assignment."""
        self.elements[key] = value
    
    def __iter__(self):
        """Support iteration."""
        return iter(self.elements)
    
    def __add__(self, other):
        """Support concatenation of ArrObjects with + operator."""
        if isinstance(other, ArrObject):
            return ArrObject(self.elements + other.elements)
        elif isinstance(other, list):
            return ArrObject(self.elements + other)
        else:
            raise TypeErrorLyric(f"unsupported operand type(s) for +: 'arr' and '{type(other).__name__}'")


class MapObject:
    """Represents a map (dictionary) object with methods."""
    
    def __init__(self, elements: dict = None):
        """Initialize MapObject with a dictionary."""
        self.elements = elements if elements is not None else {}
    
    def clear(self) -> None:
        """Remove all items from the dictionary."""
        self.elements.clear()
    
    def copy(self) -> 'MapObject':
        """Return a shallow copy of the dictionary."""
        return MapObject(self.elements.copy())
    
    @staticmethod
    def fromkeys(seq, value=None) -> 'MapObject':
        """Create a new dictionary from a sequence of keys with optional default value."""
        if isinstance(seq, ArrObject):
            seq = seq.elements
        new_dict = dict.fromkeys(seq, value)
        return MapObject(new_dict)
    
    def get(self, key: Any, default=None) -> Any:
        """Return value for key; return default if key not found."""
        return self.elements.get(key, default)
    
    def items(self) -> 'ArrObject':
        """Return an ArrObject of (key, value) pairs."""
        return ArrObject(list(self.elements.items()))
    
    def keys(self) -> 'ArrObject':
        """Return an ArrObject of all keys."""
        return ArrObject(list(self.elements.keys()))
    
    def pop(self, key: Any, *args) -> Any:
        """Remove and return value for key; raise KeyError if missing and no default."""
        if len(args) > 1:
            raise TypeErrorLyric("pop() accepts at most 2 arguments (key and default)")
        try:
            if len(args) == 0:
                # No default provided
                return self.elements.pop(key)
            else:
                # Default provided
                return self.elements.pop(key, args[0])
        except KeyError:
            raise KeyErrorLyric(f"Key '{key}' not found in map")
    
    def popitem(self) -> 'ArrObject':
        """Remove and return the last inserted (key, value) pair as an ArrObject."""
        if not self.elements:
            raise KeyErrorLyric("popitem(): map is empty")
        try:
            key, value = self.elements.popitem()
            return ArrObject([key, value])
        except KeyError:
            raise KeyErrorLyric("popitem(): map is empty")
    
    def setdefault(self, key: Any, default=None) -> Any:
        """Return value for key; if missing, insert key with default and return default."""
        return self.elements.setdefault(key, default)
    
    def update(self, other) -> None:
        """Update dictionary with key-value pairs from another dict."""
        if isinstance(other, MapObject):
            self.elements.update(other.elements)
        elif isinstance(other, dict):
            self.elements.update(other)
        else:
            raise TypeErrorLyric(f"update() expects a map or dict, got {type(other).__name__}")
    
    def values(self) -> 'ArrObject':
        """Return an ArrObject of all values."""
        return ArrObject(list(self.elements.values()))
    
    def len(self) -> int:
        """Return number of items in the dictionary."""
        return len(self.elements)
    
    def sorted(self, reverse=False) -> 'ArrObject':
        """Return an ArrObject of sorted keys."""
        try:
            return ArrObject(sorted(self.elements.keys(), reverse=reverse))
        except TypeError as e:
            raise TypeErrorLyric(f"sorted() error: {e}")
    
    def __repr__(self):
        return str(self.elements)
    
    def __str__(self):
        return str(self.elements)
    
    def __len__(self):
        return len(self.elements)
    
    def __getitem__(self, key):
        """Support indexing."""
        if key not in self.elements:
            raise KeyErrorLyric(f"Key '{key}' not found in map")
        return self.elements[key]
    
    def __setitem__(self, key, value):
        """Support item assignment."""
        self.elements[key] = value
    
    def __contains__(self, key):
        """Support 'in' operator for membership check."""
        return key in self.elements
    
    def __iter__(self):
        """Support iteration (yields keys in insertion order)."""
        return iter(self.elements)


class DskObject:
    """Represents a dsk (disk/file) object with file operations."""
    
    def __init__(self, filepath: str):
        """Initialize DskObject with a file path."""
        self.filepath = filepath
        self.file_handle = None
    
    def open(self, mode: str = 'r') -> 'DskObject':
        """Open the file in specified mode.
        
        Args:
            mode: File mode ('r', 'w', 'a', 'r+', 'w+', 'a+', 'rb', 'wb', 'ab')
                 Default is 'r' (read text)
        
        Returns:
            self for method chaining
        """
        try:
            self.file_handle = open(self.filepath, mode)
            return self
        except FileNotFoundError:
            from lyric.errors import RuntimeErrorLyric
            raise RuntimeErrorLyric(f"File not found: '{self.filepath}'")
        except PermissionError:
            from lyric.errors import RuntimeErrorLyric
            raise RuntimeErrorLyric(f"Permission denied: '{self.filepath}'")
        except Exception as e:
            from lyric.errors import RuntimeErrorLyric
            raise RuntimeErrorLyric(f"Error opening file '{self.filepath}': {e}")
    
    def close(self) -> None:
        """Close the file if it's open."""
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None
    
    def readlines(self) -> 'ArrObject':
        """Read all lines from the file and return as an ArrObject.
        
        Returns:
            ArrObject containing all lines (with newlines stripped)
        """
        if not self.file_handle:
            # Auto-open in read mode if not open
            self.open('r')
        
        try:
            lines = [line.rstrip('\n\r') for line in self.file_handle.readlines()]
            return ArrObject(lines)
        except Exception as e:
            from lyric.errors import RuntimeErrorLyric
            raise RuntimeErrorLyric(f"Error reading file '{self.filepath}': {e}")
    
    def read(self) -> str:
        """Read entire file content as a string."""
        if not self.file_handle:
            # Auto-open in read mode if not open
            self.open('r')
        
        try:
            return self.file_handle.read()
        except Exception as e:
            from lyric.errors import RuntimeErrorLyric
            raise RuntimeErrorLyric(f"Error reading file '{self.filepath}': {e}")
    
    def write(self, content: str) -> None:
        """Write content to file (overwrites existing content).
        
        Args:
            content: String content to write
        """
        if not self.file_handle:
            # Auto-open in write mode if not open
            self.open('w')
        
        try:
            self.file_handle.write(str(content))
            self.file_handle.flush()
        except Exception as e:
            from lyric.errors import RuntimeErrorLyric
            raise RuntimeErrorLyric(f"Error writing to file '{self.filepath}': {e}")
    
    def append(self, content: str) -> None:
        """Append content to file.
        
        Args:
            content: String content to append
        """
        # Close current handle if open
        if self.file_handle:
            self.close()
        
        try:
            # Open in append mode
            with open(self.filepath, 'a') as f:
                f.write(str(content))
        except Exception as e:
            from lyric.errors import RuntimeErrorLyric
            raise RuntimeErrorLyric(f"Error appending to file '{self.filepath}': {e}")
    
    def overwrite(self, content: str) -> None:
        """Overwrite file content (always opens in 'w' mode).
        
        This is used by the -> file operator to ensure consistent overwriting behavior.
        
        Args:
            content: String content to write
        """
        # Close current handle if open (to ensure we overwrite)
        if self.file_handle:
            self.close()
        
        try:
            # Always open in write mode to overwrite
            with open(self.filepath, 'w') as f:
                f.write(str(content))
        except Exception as e:
            from lyric.errors import RuntimeErrorLyric
            raise RuntimeErrorLyric(f"Error overwriting file '{self.filepath}': {e}")
    
    def delete(self) -> None:
        """Delete the file."""
        import os
        
        # Close file if open
        if self.file_handle:
            self.close()
        
        try:
            if os.path.exists(self.filepath):
                os.remove(self.filepath)
            else:
                from lyric.errors import RuntimeErrorLyric
                raise RuntimeErrorLyric(f"File not found: '{self.filepath}'")
        except Exception as e:
            from lyric.errors import RuntimeErrorLyric
            raise RuntimeErrorLyric(f"Error deleting file '{self.filepath}': {e}")
    
    def exists(self) -> bool:
        """Check if file exists."""
        import os
        return os.path.exists(self.filepath)
    
    def copy(self, to_path: str) -> None:
        """Copy file to a new location.
        
        Args:
            to_path: Destination path
        """
        import shutil
        
        try:
            shutil.copy2(self.filepath, to_path)
        except FileNotFoundError:
            from lyric.errors import RuntimeErrorLyric
            raise RuntimeErrorLyric(f"File not found: '{self.filepath}'")
        except Exception as e:
            from lyric.errors import RuntimeErrorLyric
            raise RuntimeErrorLyric(f"Error copying file '{self.filepath}' to '{to_path}': {e}")
    
    def move(self, to_path: str) -> None:
        """Move file to a new location.
        
        Args:
            to_path: Destination path
        """
        import shutil
        
        # Close file if open
        if self.file_handle:
            self.close()
        
        try:
            shutil.move(self.filepath, to_path)
            # Update the filepath
            self.filepath = to_path
        except FileNotFoundError:
            from lyric.errors import RuntimeErrorLyric
            raise RuntimeErrorLyric(f"File not found: '{self.filepath}'")
        except Exception as e:
            from lyric.errors import RuntimeErrorLyric
            raise RuntimeErrorLyric(f"Error moving file '{self.filepath}' to '{to_path}': {e}")
    
    def size(self) -> int:
        """Get file size in bytes."""
        import os
        
        try:
            return os.path.getsize(self.filepath)
        except FileNotFoundError:
            from lyric.errors import RuntimeErrorLyric
            raise RuntimeErrorLyric(f"File not found: '{self.filepath}'")
        except Exception as e:
            from lyric.errors import RuntimeErrorLyric
            raise RuntimeErrorLyric(f"Error getting size of file '{self.filepath}': {e}")
    
    def __repr__(self):
        return f"dsk('{self.filepath}')"
    
    def __str__(self):
        return self.filepath
    
    def __del__(self):
        """Destructor: close file if still open."""
        if self.file_handle:
            try:
                self.file_handle.close()
            except:
                pass


class ReturnValue:
    """Wrapper for return values to distinguish them from normal expression values."""
    def __init__(self, value):
        self.value = value


class Interpreter:
    """Interpreter for executing Lyric AST nodes."""
    
    def __init__(self, source_file=None):
        self.global_scope = {
            'true': True,
            'false': False,
            'None': None
        }
        # Track variable types with scope support
        self.variable_types = {}  # Global scope
        self.scope_stack = []     # Stack of scopes for nested functions/blocks
        # Register built-in functions
        register_builtins(self.global_scope)
        self.functions = {}
        self.classes = {}
        # Track the source file path for relative imports
        self.source_file = source_file
        # Track the current instance context for access control
        self.current_instance = None
        # Track the current class name for constructor context
        self.current_class_name = None
        # Store command-line arguments for main() function
        self.cli_args = []
    
    def _push_scope(self):
        """Push a new scope onto the stack."""
        self.scope_stack.append({})
    
    def _pop_scope(self):
        """Pop the current scope from the stack."""
        if self.scope_stack:
            return self.scope_stack.pop()
        return {}
    
    def _get_current_scope(self):
        """Get the current scope (top of stack) or global scope."""
        if self.scope_stack:
            return self.scope_stack[-1]
        return self.variable_types
    
    def _is_variable_declared_in_any_scope(self, var_name: str) -> bool:
        """Check if a variable is declared in any scope (current or parent)."""
        # Check current scope first
        if var_name in self._get_current_scope():
            return True
        
        # Check parent scopes
        for scope in reversed(self.scope_stack[:-1]):
            if var_name in scope:
                return True
        
        # Check global scope
        if var_name in self.variable_types:
            return True
        
        return False
    
    def _set_variable_in_current_scope(self, var_name: str, var_type: str):
        """Set a variable in the current scope."""
        current_scope = self._get_current_scope()
        current_scope[var_name] = var_type
    
    def _get_variable_type(self, var_name: str) -> str:
        """Get the declared type of a variable."""
        # Check all scopes from innermost to outermost
        for scope in reversed(self.scope_stack):
            if var_name in scope:
                return scope[var_name]
        
        # Check global scope
        if var_name in self.variable_types:
            return self.variable_types[var_name]
        
        # Not found - return 'var' as default
        return 'var'
    
    def _infer_function_return_type(self, func_node: FunctionNode) -> str:
        """Infer the return type of a function by analyzing all return statements."""
        return_types = []
        has_explicit_return = False
        has_implicit_return = False
        
        # Analyze all statements in the function body recursively
        for stmt in func_node.body_statements:
            return_types.extend(self._find_return_statements(stmt))
        
        # Check if we found any return statements
        if return_types:
            has_explicit_return = True
        else:
            has_implicit_return = True
            return_types.append('None')
        
        # Check for consistency
        unique_types = set(return_types)
        if len(unique_types) > 1:
            # Allow int and flt to be compatible (both return flt)
            if unique_types == {'int', 'flt'}:
                return 'flt'  # If both int and flt, return flt
            else:
                raise CompileErrorLyric(
                    f"Inconsistent return types in function '{func_node.name}': {unique_types}",
                    func_node.line, func_node.column
                )
        
        return return_types[0] if return_types else 'None'
    
    def _find_return_statements(self, stmt) -> List[str]:
        """Recursively find all return statements in a statement."""
        return_types = []
        
        if isinstance(stmt, ReturnNode):
            if stmt.value is None:
                return_types.append('None')
            else:
                return_type = self._analyze_expression_type(stmt.value)
                return_types.append(return_type)
        elif isinstance(stmt, IfNode):
            # Check then clause
            if stmt.then_body:
                for then_stmt in stmt.then_body:
                    return_types.extend(self._find_return_statements(then_stmt))
            # Check elif clauses
            if stmt.elifs:
                for elif_clause in stmt.elifs:
                    # elif_clause is a tuple of (condition, body)
                    if isinstance(elif_clause, tuple) and len(elif_clause) > 1:
                        for elif_stmt in elif_clause[1]:
                            return_types.extend(self._find_return_statements(elif_stmt))
            # Check else clause
            if stmt.else_body:
                for else_stmt in stmt.else_body:
                    return_types.extend(self._find_return_statements(else_stmt))
        elif isinstance(stmt, TryNode):
            # Check try block
            if stmt.try_body:
                for try_stmt in stmt.try_body:
                    return_types.extend(self._find_return_statements(try_stmt))
            # Check catch block
            for catch_clause in stmt.catch_clauses:
                for catch_stmt in catch_clause.body:
                    return_types.extend(self._find_return_statements(catch_stmt))
            # Check finally block
            if stmt.finally_body:
                for finally_stmt in stmt.finally_body:
                    return_types.extend(self._find_return_statements(finally_stmt))
        elif isinstance(stmt, LoopNode):
            # Check loop body
            if stmt.body:
                for loop_stmt in stmt.body:
                    return_types.extend(self._find_return_statements(loop_stmt))
        
        return return_types
    
    def _analyze_expression_type(self, expr) -> str:
        """Analyze the type of an expression without evaluating it."""
        if isinstance(expr, LiteralNode):
            if isinstance(expr.value, bool):
                return 'god'
            elif isinstance(expr.value, int):
                return 'int'
            elif isinstance(expr.value, float):
                return 'flt'
            elif isinstance(expr.value, str):
                return 'str'
            elif expr.value is None:
                return 'None'
            else:
                return 'var'
        elif isinstance(expr, IdentifierNode):
            # For now, we can't determine the type without evaluation
            # This is a limitation of static analysis
            return 'var'
        elif isinstance(expr, BinaryOpNode):
            # For binary operations, we need to analyze both operands
            left_type = self._analyze_expression_type(expr.left)
            right_type = self._analyze_expression_type(expr.right)
            
            # Simple type inference for common operations
            if expr.op in ['+', '-', '*']:
                if left_type == 'str' or right_type == 'str':
                    return 'str'  # String concatenation
                elif left_type == 'flt' or right_type == 'flt':
                    return 'flt'  # Float arithmetic
                elif left_type == 'int' and right_type == 'int':
                    return 'int'  # Integer arithmetic
                else:
                    return 'var'  # Mixed types default to var
            elif expr.op == '/':
                # Division always returns float in Lyric
                if left_type == 'str' or right_type == 'str':
                    return 'var'  # Invalid operation
                else:
                    return 'flt'  # Division always returns float
            elif expr.op in ['==', '!=', '<', '>', '<=', '>=']:
                return 'god'  # Comparison operations return boolean
            else:
                return 'var'  # Default to var for unknown operations
        elif isinstance(expr, UnaryOpNode):
            operand_type = self._analyze_expression_type(expr.operand)
            if expr.op == 'not':
                return 'god'  # Logical not returns boolean
            elif expr.op in ['-', '+']:
                return operand_type  # Unary plus/minus preserves type
            else:
                return 'var'
        elif isinstance(expr, CallNode):
            # Function calls - we can't determine return type without knowing the function
            return 'var'
        elif isinstance(expr, ListLiteralNode):
            return 'var'  # Lists are var type
        elif isinstance(expr, DictLiteralNode):
            return 'var'  # Dictionaries are var type
        elif isinstance(expr, RexNode):
            return 'rex'  # Regex literals
        else:
            return 'var'  # Default to var for unknown expressions
    
    def _is_type_compatible(self, expected_type: str, value: Any) -> bool:
        """Check if a value is compatible with the expected type."""
        if expected_type == 'var':
            return True
        
        if expected_type == 'None':
            return value is None
        
        if expected_type == 'int':
            return isinstance(value, int)
        elif expected_type == 'flt':
            return isinstance(value, (int, float))  # Allow int to be assigned to float
        elif expected_type == 'str':
            return isinstance(value, str)
        elif expected_type == 'god':
            return isinstance(value, bool)
        elif expected_type == 'bin':
            return isinstance(value, (int, bool))  # Allow int and bool for bin
        elif expected_type == 'rex':
            # Check if it's a regex object (we'll need to import the RexObject class)
            try:
                from lyric.runtime import RexObject
                return isinstance(value, RexObject)
            except ImportError:
                return False
        elif expected_type == 'pyobject':
            return True  # pyobject can hold any Python object
        elif expected_type == 'arr':
            return isinstance(value, list)  # arr maps to Python list
        elif expected_type == 'map':
            return isinstance(value, dict)  # map maps to Python dict
        
        return False
    
    def evaluate(self, ast: ProgramNode) -> Any:
        """Evaluate a ProgramNode and return the result."""
        try:
            # Evaluate all statements in the program
            for statement in ast.statements:
                self._evaluate_statement(statement)
            
            # If there's a main function, call it and return its result
            if "main" in self.functions:
                # Prepare arguments for main()
                main_func = self.functions["main"]
                main_params = main_func['params']
                
                # If main() expects parameters (argc, argv), provide them
                if len(main_params) >= 2:
                    # Import ArrObject here to avoid circular imports
                    from lyric.interpreter import ArrObject
                    
                    # Create argc (number of arguments) and argv (array of arguments)
                    argc = len(self.cli_args)
                    argv = ArrObject(self.cli_args)
                    
                    return self._call_function("main", [argc, argv])
                elif len(main_params) == 0:
                    # main() has no parameters
                    return self._call_function("main", [])
                else:
                    # main() has 1 parameter - not a standard pattern, but allow it
                    return self._call_function("main", [len(self.cli_args)])
            
            return None
        except Exception as e:
            if isinstance(e, RuntimeErrorLyric):
                raise
            # Convert Python exceptions to Lyric exceptions
            if isinstance(e, IndexError):
                raise IndexErrorLyric(str(e))
            if isinstance(e, KeyError):
                raise KeyErrorLyric(str(e))
            if isinstance(e, TypeError):
                raise TypeErrorLyric(str(e))
            if isinstance(e, ValueError):
                raise ValueErrorLyric(str(e))
            if isinstance(e, AttributeError):
                raise AttributeErrorLyric(str(e))
            if isinstance(e, ZeroDivisionError):
                raise ZeroDivisionErrorLyric(str(e))
            raise RuntimeErrorLyric(str(e))
    
    def _call_function(self, func_name: str, args: List[Any]) -> Any:
        """Call a function by name with arguments."""
        if func_name in self.functions:
            func_def = self.functions[func_name]
            params = func_def['params']
            param_types = func_def.get('param_types', [])
            return_type = func_def.get('return_type', 'var')
            body = func_def['body']
            module_scope = func_def.get('module_scope', None)  # Get module scope if available
            
            # Create local scope
            local_scope = {}
            for i, param in enumerate(params):
                if i < len(args):
                    arg_value = args[i]
                else:
                    arg_value = None
                
                # Type enforcement for parameters
                if i < len(param_types) and param_types[i] != 'var':
                    if arg_value is None:
                        raise RuntimeErrorLyric(
                            f"Type error: parameter '{param}' expects {param_types[i]}, got None"
                        )
                    elif not self._is_type_compatible(param_types[i], arg_value):
                        raise RuntimeErrorLyric(
                            f"Type error: parameter '{param}' expects {param_types[i]}, got {type(arg_value).__name__}"
                        )
                
                local_scope[param] = arg_value
            
            # Save current scope
            old_scope = self.global_scope.copy()
            
            # If function has a module scope, use it as the base scope
            if module_scope is not None:
                self.global_scope = module_scope.copy()
            
            # Set local scope (parameters override module scope)
            self.global_scope.update(local_scope)
            
            # Push function scope for variable types
            self._push_scope()
            
            try:
                # Execute function body
                result = None
                for statement in body:
                    result = self._evaluate_statement(statement)
                    if isinstance(result, ReturnValue):
                        return_value = result.value
                        # Validate return type
                        if return_type != 'var' and not self._is_type_compatible(return_type, return_value):
                            raise RuntimeErrorLyric(
                                f"Type error: return value does not match declared type. "
                                f"Expected {return_type}, but got {type(return_value).__name__}"
                            )
                        return return_value
                
                # If no explicit return, return None
                if return_type != 'var' and return_type != 'None':
                    raise RuntimeErrorLyric(
                        f"Type error: function '{func_name}' declared to return {return_type}, but returns None"
                    )
                return None
            finally:
                # Restore scope
                self.global_scope = old_scope
                self._pop_scope()
        else:
            raise RuntimeErrorLyric(f"Function '{func_name}' is not defined")
    
    def _is_derived_from(self, child_class: str, parent_class: str) -> bool:
        """Check if child_class is derived from parent_class."""
        if child_class not in self.classes:
            return False
        
        current = child_class
        while current:
            if current == parent_class:
                return True
            class_def = self.classes.get(current)
            if not class_def:
                return False
            current = class_def.get('__base_class__')
        
        return False
    
    def _check_attribute_access(self, instance: dict, attr_name: str) -> None:
        """Check if attribute access is allowed based on visibility modifier.
        
        Args:
            instance: The class instance
            attr_name: Name of the attribute being accessed
        """
        # Skip access check for special attributes
        if attr_name.startswith('__'):
            return
        
        # Get the visibility of the attribute
        visibility_key = f'__visibility_{attr_name}__'
        visibility = instance.get(visibility_key, 'public')
        
        # Public attributes are always accessible
        if visibility == 'public':
            return
        
        # Determine caller context
        caller_context = 'external'
        if self.current_instance is not None:
            # We're inside a method call
            # Use current_class_name if set (for constructor context), otherwise use instance's class
            current_class = self.current_class_name if self.current_class_name is not None else self.current_instance.get('__instance_class__')
            target_class = instance.get('__instance_class__')
            
            # Check if calling from same instance
            if instance is self.current_instance:
                # Accessing attributes of self - context depends on class hierarchy
                if current_class == target_class:
                    caller_context = 'internal'
                elif self._is_derived_from(current_class, target_class):
                    caller_context = 'derived'
                elif self._is_derived_from(target_class, current_class):
                    # Target class derives from current class (e.g., Base constructor accessing Child instance)
                    # This is 'internal' for attributes defined in current class
                    caller_context = 'internal'
                else:
                    caller_context = 'external'
            elif current_class == target_class:
                caller_context = 'internal'
            elif self._is_derived_from(current_class, target_class):
                caller_context = 'derived'
            else:
                caller_context = 'external'
        
        # For private attributes, we need additional checking
        if visibility == 'private':
            # Even if caller_context is 'internal', we need to verify the attribute
            # is defined in the caller's class, not inherited from a base class
            if caller_context == 'internal':
                # Get the caller's class
                caller_class = self.current_class_name if self.current_class_name is not None else (self.current_instance.get('__instance_class__') if self.current_instance else None)
                # Check if the attribute is defined in the caller's class (not inherited)
                if caller_class and caller_class in self.classes:
                    class_def = self.classes[caller_class]
                    # If the attribute's visibility key is not in this class's definition, it's inherited
                    if visibility_key not in class_def:
                        # Attribute is inherited from a base class, and it's private, so deny access
                        raise RuntimeErrorLyric(
                            f"Access error: Cannot access private attribute '{attr_name}' inherited from base class. "
                            f"Private attributes can only be accessed from within the class where they are defined."
                        )
                # If we get here, the attribute is in the caller's class, so allow access
                return
            else:
                # Called from outside the class or from a derived class
                class_name = instance.get('__instance_class__', 'Unknown')
                raise RuntimeErrorLyric(
                    f"Access error: Cannot access private attribute '{attr_name}' of class '{class_name}'. "
                    f"Private attributes can only be accessed from within the same class."
                )
        
        # Protected attributes can be accessed from the same class or derived classes
        if visibility == 'protected' and caller_context not in ('internal', 'derived'):
            class_name = instance.get('__instance_class__', 'Unknown')
            raise RuntimeErrorLyric(
                f"Access error: Cannot access protected attribute '{attr_name}' of class '{class_name}'. "
                f"Protected attributes can only be accessed from the same class or derived classes."
            )
    
    def _is_derived_from(self, child_class: str, base_class: str) -> bool:
        """Check if child_class is derived from base_class."""
        if child_class == base_class:
            return False  # Same class, not derived
        
        # Walk up the inheritance chain
        current = child_class
        while current in self.classes:
            class_def = self.classes[current]
            if '__base_class__' in class_def:
                parent = class_def['__base_class__']
                if parent == base_class:
                    return True
                current = parent
            else:
                break
        return False
    
    def _find_method_defining_class(self, instance: dict, method_name: str) -> str:
        """Find which class in the inheritance chain defines a given method.
        
        Args:
            instance: The instance dictionary
            method_name: The name of the method to find
            
        Returns:
            The name of the class that defines the method, or the instance's class if not found
        """
        # Start from the instance's class
        instance_class = instance.get('__instance_class__')
        if not instance_class:
            return None
        
        # Walk up the inheritance chain to find where the method is defined
        current_class = instance_class
        while current_class in self.classes:
            class_def = self.classes[current_class]
            if method_name in class_def and isinstance(class_def[method_name], dict) and 'body' in class_def[method_name]:
                # Found the method definition in this class
                return current_class
            
            # Move to base class
            if '__base_class__' in class_def:
                current_class = class_def['__base_class__']
            else:
                break
        
        # Method not found in class hierarchy, return instance class as fallback
        return instance_class
    
    def _check_method_access(self, instance: dict, method_name: str, method_def: dict, caller_context: str = 'external') -> None:
        """Check if method access is allowed based on visibility modifier.
        
        Args:
            instance: The class instance
            method_name: Name of the method being accessed
            method_def: Method definition dictionary
            caller_context: 'internal' if called from same class, 'derived' if from derived class, 'external' otherwise
        """
        visibility = method_def.get('visibility', 'public')
        
        # Public methods are always accessible
        if visibility == 'public':
            return
        
        # For private methods, we need additional checking
        if visibility == 'private':
            # Even if caller_context is 'internal', we need to verify the method
            # is defined in the caller's class, not inherited from a base class
            if caller_context == 'internal':
                # Get the caller's class
                caller_class = self.current_instance.get('__instance_class__') if self.current_instance else None
                # Check if the method is defined in the caller's class (not inherited)
                if caller_class and caller_class in self.classes:
                    class_def = self.classes[caller_class]
                    # If the method is not in this class's definition, it's inherited
                    if method_name not in class_def:
                        # Method is inherited from a base class, and it's private, so deny access
                        raise RuntimeErrorLyric(
                            f"Access error: Cannot access private method '{method_name}' inherited from base class. "
                            f"Private methods can only be called from within the class where they are defined."
                        )
                # If we get here, the method is in the caller's class, so allow access
                return
            else:
                # Called from outside the class
                class_name = instance.get('__instance_class__', 'Unknown')
                raise RuntimeErrorLyric(
                    f"Access error: Cannot access private method '{method_name}' of class '{class_name}'. "
                    f"Private methods can only be called from within the same class."
                )
        
        # Protected methods can be called from the same class or derived classes
        if visibility == 'protected' and caller_context not in ('internal', 'derived'):
            class_name = instance.get('__instance_class__', 'Unknown')
            raise RuntimeErrorLyric(
                f"Access error: Cannot access protected method '{method_name}' of class '{class_name}'. "
                f"Protected methods can only be called from the same class or derived classes."
            )
    
    def _call_method(self, instance: dict, method: dict, args: List[Any], class_context: str = None) -> Any:
        """Call a method on an instance.
        
        Args:
            instance: The instance dictionary
            method: The method dictionary containing params, body, etc.
            args: Arguments to pass to the method
            class_context: Optional class name to use as the execution context (for constructors)
        """
        params = method['params']
        param_types = method.get('param_types', [])
        body = method['body']
        
        # Create local scope with 'self' pointing to the instance
        local_scope = {'self': instance}
        
        # Add method parameters
        for i, param in enumerate(params):
            if i < len(args):
                arg_value = self._evaluate_expression(args[i])
            else:
                arg_value = None
            
            # Type enforcement for parameters
            if i < len(param_types) and param_types[i] != 'var':
                if arg_value is None:
                    raise RuntimeErrorLyric(
                        f"Type error: parameter '{param}' expects {param_types[i]}, got None"
                    )
                elif not self._is_type_compatible(param_types[i], arg_value):
                    raise RuntimeErrorLyric(
                        f"Type error: parameter '{param}' expects {param_types[i]}, got {type(arg_value).__name__}"
                    )
            
            local_scope[param] = arg_value
        
        # Save current scope and instance context
        old_scope = self.global_scope.copy()
        old_instance = self.current_instance
        old_class_name = self.current_class_name
        
        # Set local scope and current instance/class for method execution
        self.global_scope.update(local_scope)
        self.current_instance = instance
        # Use provided class_context if available (for constructors), otherwise use instance's class
        self.current_class_name = class_context if class_context is not None else instance.get('__instance_class__')
        
        # Push method scope for variable types
        self._push_scope()
        
        try:
            # Execute method body
            result = None
            for statement in body:
                result = self._evaluate_statement(statement)
                if isinstance(result, ReturnValue):
                    return result.value
            # If no explicit return, return the last statement result
            return result if not isinstance(result, ReturnValue) else result.value
        finally:
            # Restore scope and instance context
            self.global_scope = old_scope
            self.current_instance = old_instance
            self.current_class_name = old_class_name
            self._pop_scope()
    
    
    def _evaluate_statement(self, statement) -> Any:
        """Evaluate a single statement."""
        if isinstance(statement, TypeDeclarationNode):
            return self._evaluate_type_declaration(statement)
        elif isinstance(statement, MultiDeclarationNode):
            return self._evaluate_multi_declaration(statement)
        elif isinstance(statement, AssignNode):
            return self._evaluate_assignment(statement)
        elif isinstance(statement, FunctionNode):
            return self._evaluate_function_definition(statement)
        elif isinstance(statement, ClassNode):
            return self._evaluate_class_definition(statement)
        elif isinstance(statement, IfNode):
            return self._evaluate_if_statement(statement)
        elif isinstance(statement, LoopNode):
            return self._evaluate_loop_statement(statement)
        elif isinstance(statement, CallNode):
            return self._evaluate_function_call(statement)
        elif isinstance(statement, ReturnNode):
            return self._evaluate_return_statement(statement)
        elif isinstance(statement, BreakNode):
            return self._evaluate_break_statement(statement)
        elif isinstance(statement, ContinueNode):
            return self._evaluate_continue_statement(statement)
        elif isinstance(statement, TryNode):
            return self._evaluate_try_statement(statement)
        elif isinstance(statement, RaiseNode):
            return self._evaluate_raise_statement(statement)
        elif isinstance(statement, ImportNode):
            return self._evaluate_import_statement(statement)
        elif isinstance(statement, ImportPyNode):
            return self._evaluate_importpy_statement(statement)
        elif isinstance(statement, FileOpNode):
            return self._evaluate_file_op(statement)
        else:
            # Expression statement
            return self._evaluate_expression(statement)
    
    def _evaluate_assignment(self, node: AssignNode) -> Any:
        """Evaluate an assignment statement."""
        value = self._evaluate_expression(node.expr)
        
        if '.' in node.name:
            # Assignment to member: self.attribute = value
            parts = node.name.split('.')
            obj_name = parts[0]
            member_name = parts[1]
            
            if obj_name in self.global_scope:
                obj = self.global_scope[obj_name]
                if isinstance(obj, dict):
                    obj[member_name] = value
                else:
                    raise RuntimeErrorLyric(f"Cannot assign to member of non-object '{obj_name}'")
            else:
                raise RuntimeErrorLyric(f"Variable '{obj_name}' is not defined")
        elif '[' in node.name and ']' in node.name:
            # Assignment to indexed expression: obj[index] = value
            # Parse the indexed assignment
            bracket_start = node.name.find('[')
            bracket_end = node.name.find(']')
            obj_name = node.name[:bracket_start]
            index_str = node.name[bracket_start+1:bracket_end]
            
            if obj_name in self.global_scope:
                obj = self.global_scope[obj_name]
                if isinstance(obj, (dict, MapObject)):
                    # For dictionaries and MapObject, the index is a key
                    obj[index_str] = value
                elif isinstance(obj, (list, ArrObject)):
                    # For lists and ArrObject, the index should be an integer
                    try:
                        index = int(index_str)
                        obj_len = len(obj.elements) if isinstance(obj, ArrObject) else len(obj)
                        if index < 0 or index >= obj_len:
                            raise IndexErrorLyric(f"Index out of range: tried to access index {index} in list of length {obj_len}. Valid indices are 0 to {obj_len-1}", node.line, node.column)
                        obj[index] = value
                    except ValueError:
                        raise RuntimeErrorLyric(f"Invalid list index: '{index_str}' is not a valid integer. List indices must be integers.", node.line, node.column)
                else:
                    raise RuntimeErrorLyric(f"Cannot assign to indexed expression: '{obj_name}' is of type {type(obj).__name__}, but only lists and dictionaries support indexed assignment", node.line, node.column)
            else:
                raise RuntimeErrorLyric(f"Undefined variable: '{obj_name}' has not been declared. Use a type declaration (int, str, flt, var) or assign a value first", node.line, node.column)
        else:
            # Regular assignment
            # Check type enforcement if variable was declared with a type in any scope
            var_type = None
            # Check current scope first
            current_scope = self._get_current_scope()
            if node.name in current_scope:
                var_type = current_scope[node.name]
            else:
                # Check parent scopes
                for scope in reversed(self.scope_stack[:-1]):
                    if node.name in scope:
                        var_type = scope[node.name]
                        break
                # Check global scope
                if var_type is None and node.name in self.variable_types:
                    var_type = self.variable_types[node.name]
            
            if var_type and var_type != 'var' and not self._is_type_compatible(var_type, value):
                raise RuntimeErrorLyric(
                    f"Type mismatch: cannot assign {type(value).__name__} to variable '{node.name}' declared as {var_type}. "
                    f"Expected {var_type}, but got {type(value).__name__}. "
                    f"Use 'var {node.name} = ...' if you need dynamic typing.",
                    node.line, node.column
                )
            
            self.global_scope[node.name] = value
        
        return value
    
    def _evaluate_type_declaration(self, node: TypeDeclarationNode) -> Any:
        """Evaluate a type declaration statement."""
        # Check for redeclaration in current scope only
        if node.name in self._get_current_scope():
            raise CompileErrorLyric(
                f"Variable '{node.name}' already declared",
                node.line, node.column
            )
        
        value = self._evaluate_expression(node.expr)
        
        # Store the variable type in current scope
        self._set_variable_in_current_scope(node.name, node.type_name)
        
        # Type enforcement for strict types
        if node.type_name != 'var':
            if not self._is_type_compatible(node.type_name, value):
                raise RuntimeErrorLyric(
                    f"Type mismatch: cannot assign {type(value).__name__} to variable '{node.name}' declared as {node.type_name}. "
                    f"Expected {node.type_name}, but got {type(value).__name__}. "
                    f"Use 'var {node.name} = ...' if you need dynamic typing.",
                    node.line, node.column
                )
        
        # Store the value
        self.global_scope[node.name] = value
        return value
    
    def _evaluate_multi_declaration(self, node: MultiDeclarationNode) -> Any:
        """Evaluate a multi-variable declaration statement."""
        # Check for redeclarations in current scope first
        for type_name, var_name in node.declarations:
            if var_name in self._get_current_scope():
                raise CompileErrorLyric(
                    f"Variable '{var_name}' already declared",
                    node.line, node.column
                )
        
        # Declare all variables as uninitialized in current scope
        for type_name, var_name in node.declarations:
            # Store the variable type in current scope
            self._set_variable_in_current_scope(var_name, type_name)
            
            # Declare the variable as uninitialized (None)
            self.global_scope[var_name] = None
        
        return None
    
    def _is_type_compatible(self, expected_type: str, value: Any) -> bool:
        """Check if a value is compatible with the expected type."""
        if expected_type == 'var':
            return True  # var accepts any type, including pyobject
        elif expected_type == 'pyobject':
            # pyobject internally maps to var in Lyric syntax
            return True  # pyobject can hold any Python value
        elif expected_type == 'int':
            return isinstance(value, int) and not isinstance(value, bool)
        elif expected_type == 'str':
            return isinstance(value, str)
        elif expected_type == 'flt':
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        elif expected_type == 'rex':
            return isinstance(value, RexObject)
        elif expected_type == 'god':
            return isinstance(value, bool)
        elif expected_type == 'bin':
            return isinstance(value, bool)  # bin is an alias for god
        elif expected_type == 'arr':
            return isinstance(value, (list, ArrObject))  # arr maps to ArrObject or Python list
        elif expected_type == 'map':
            return isinstance(value, (dict, MapObject))  # map maps to MapObject or Python dict
        elif expected_type == 'dsk':
            return isinstance(value, DskObject)  # dsk maps to DskObject
        elif expected_type == 'obj':
            # obj is for class instances - check if it's a dict with __instance_class__ marker
            return isinstance(value, dict) and '__instance_class__' in value
        else:
            return False
    
    def _evaluate_return_statement(self, node: ReturnNode) -> ReturnValue:
        """Evaluate a return statement."""
        if node.value:
            return ReturnValue(self._evaluate_expression(node.value))
        return ReturnValue(None)
    
    def _evaluate_list_literal(self, node: ListLiteralNode) -> 'ArrObject':
        """Evaluate a list literal."""
        elements = [self._evaluate_expression(elem) for elem in node.elements]
        return ArrObject(elements)
    
    def _evaluate_dict_literal(self, node: DictLiteralNode) -> 'MapObject':
        """Evaluate a dictionary literal."""
        result = {}
        for key_expr, value_expr in node.pairs:
            key = self._evaluate_expression(key_expr)
            value = self._evaluate_expression(value_expr)
            result[key] = value
        return MapObject(result)
    
    def _evaluate_index(self, node: IndexNode) -> Any:
        """Evaluate an indexing operation."""
        obj = self._evaluate_expression(node.obj)
        index = self._evaluate_expression(node.index)
        
        if isinstance(obj, (list, tuple, ArrObject)):
            if not isinstance(index, int):
                raise TypeErrorLyric(f"Invalid list index: expected integer, but got {type(index).__name__}. List indices must be integers (0, 1, 2, ...)")
            if isinstance(obj, ArrObject):
                if index < 0 or index >= len(obj.elements):
                    raise IndexErrorLyric(f"Index out of range: tried to access index {index} in arr of length {len(obj.elements)}. Valid indices are 0 to {len(obj.elements)-1}")
                return obj[index]
            else:
                if index < 0 or index >= len(obj):
                    raise IndexErrorLyric(f"Index out of range: tried to access index {index} in list of length {len(obj)}. Valid indices are 0 to {len(obj)-1}")
                return obj[index]
        elif isinstance(obj, (dict, MapObject)):
            if isinstance(obj, MapObject):
                # MapObject handles KeyError in its __getitem__
                return obj[index]
            else:
                # Plain dict
                if index not in obj:
                    available_keys = list(obj.keys())[:5]  # Show first 5 keys
                    keys_preview = ", ".join(repr(k) for k in available_keys)
                    if len(obj) > 5:
                        keys_preview += f" (and {len(obj)-5} more)"
                    raise KeyErrorLyric(f"Key not found: '{index}' is not a key in this dictionary. Available keys: {keys_preview}")
                return obj[index]
        else:
            raise TypeErrorLyric(f"Cannot index object: '{type(obj).__name__}' does not support indexing. Only lists and dictionaries can be indexed with []. Use dot notation (.) for object properties.")
    
    def _evaluate_slice(self, node: SliceNode) -> Any:
        """Evaluate a slice operation."""
        obj = self._evaluate_expression(node.obj)
        
        # Evaluate slice parameters
        start = self._evaluate_expression(node.start) if node.start else None
        end = self._evaluate_expression(node.end) if node.end else None
        step = self._evaluate_expression(node.step) if node.step else None
        
        # Handle different object types
        if isinstance(obj, (str, list, tuple)):
            try:
                return obj[start:end:step]
            except Exception as e:
                raise RuntimeErrorLyric(f"Slice operation failed: {str(e)}", node.line, node.column)
        elif isinstance(obj, ArrObject):
            try:
                # ArrObject.__getitem__ handles slicing and returns a new ArrObject
                return obj[start:end:step]
            except Exception as e:
                raise RuntimeErrorLyric(f"Slice operation failed: {str(e)}", node.line, node.column)
        else:
            raise TypeErrorLyric(f"Cannot slice object: '{type(obj).__name__}' does not support slicing. Only strings, lists, and tuples can be sliced with [start:end:step].", node.line, node.column)
    
    def _evaluate_rex_literal(self, node: RexNode) -> 'RexObject':
        """Evaluate a regex literal and return a RexObject."""
        import re
        try:
            compiled_pattern = re.compile(node.pattern)
            return RexObject(compiled_pattern)
        except re.error as e:
            raise RuntimeErrorLyric(f"Invalid regex pattern '{node.pattern}' at line {node.line}, column {node.column}: {e}")
    
    def _evaluate_function_definition(self, node: FunctionNode) -> None:
        """Evaluate a function definition."""
        # Determine return type
        if node.return_type:
            # Explicit return type declared
            return_type = node.return_type
        else:
            # Infer return type from function body
            return_type = self._infer_function_return_type(node)
        
        # Store function with return type
        self.functions[node.name] = {
            'params': node.params,
            'param_types': node.param_types,
            'return_type': return_type,
            'body': node.body_statements
        }
    
    def _evaluate_class_definition(self, node: ClassNode) -> None:
        """Evaluate a class definition."""
        class_dict = {}
        # Add a special marker to identify this as a class definition
        class_dict['__class_name__'] = node.name
        
        # Store base class name if present
        if node.base_class:
            class_dict['__base_class__'] = node.base_class
        
        # Store constructor method separately if it exists
        if node.constructor_method:
            class_dict['__constructor__'] = {
                'params': node.constructor_method.params,
                'param_types': node.constructor_method.param_types,
                'body': node.constructor_method.body_statements,
                'visibility': node.constructor_method.visibility
            }
        
        for member in node.members_statements:
            if isinstance(member, AssignNode):
                # Class member assignment (no visibility, defaults to public)
                value = self._evaluate_expression(member.expr)
                class_dict[member.name] = value
                # Store visibility metadata
                class_dict[f'__visibility_{member.name}__'] = 'public'
            elif isinstance(member, TypeDeclarationNode):
                # Type declaration in class (with visibility)
                value = self._evaluate_expression(member.expr)
                class_dict[member.name] = value
                # Store visibility metadata
                class_dict[f'__visibility_{member.name}__'] = member.visibility
            elif isinstance(member, MultiDeclarationNode):
                # Multi-variable declaration in class (with visibility)
                for type_name, var_name in member.declarations:
                    class_dict[var_name] = None  # Declare as uninitialized
                    # Store visibility metadata
                    class_dict[f'__visibility_{var_name}__'] = member.visibility
            elif isinstance(member, FunctionNode):
                # Class method
                class_dict[member.name] = {
                    'params': member.params,
                    'param_types': member.param_types,
                    'body': member.body_statements,
                    'visibility': member.visibility
                }
        
        self.classes[node.name] = class_dict
    
    def _evaluate_if_statement(self, node: IfNode) -> Any:
        """Evaluate an if statement."""
        condition = self._evaluate_expression(node.condition)
        
        if self._is_truthy(condition):
            # Execute then body
            for statement in node.then_body:
                result = self._evaluate_statement(statement)
                if isinstance(result, ReturnValue):
                    return result
        else:
            # Check elif clauses
            for elif_condition, elif_body in node.elifs:
                elif_result = self._evaluate_expression(elif_condition)
                if self._is_truthy(elif_result):
                    for statement in elif_body:
                        result = self._evaluate_statement(statement)
                        if isinstance(result, ReturnValue):
                            return result
                    return None
            
            # Execute else body if it exists
            if node.else_body:
                for statement in node.else_body:
                    result = self._evaluate_statement(statement)
                    if isinstance(result, ReturnValue):
                        return result
        
        return None
    
    def _evaluate_loop_statement(self, node: LoopNode) -> Any:
        """Evaluate a loop statement."""
        if node.loop_kind == "iterator":
            # Iterator loop: given i in range(3):
            return self._evaluate_iterator_loop(node)
        else:
            # While loop: given x > 0:
            return self._evaluate_while_loop(node)
    
    def _evaluate_iterator_loop(self, node: LoopNode) -> Any:
        """Evaluate an iterator loop."""
        # For now, handle range() calls
        if isinstance(node.condition_or_iter, CallNode) and node.condition_or_iter.func_name == "range":
            # Get the iterator variable name from the loop node
            iterator_var = node.iterator_var or 'i'
            
            # Evaluate range arguments
            args = [self._evaluate_expression(arg) for arg in node.condition_or_iter.args]
            
            if len(args) == 1:
                # range(n) -> 0 to n-1
                end = args[0]
                for i in range(end):
                    # Assign loop variable to scope
                    self.global_scope[iterator_var] = i
                    # Execute loop body
                    try:
                        for statement in node.body:
                            self._evaluate_statement(statement)
                    except BreakSignal:
                        break  # Exit loop
                    except ContinueSignal:
                        continue  # Skip to next iteration
            elif len(args) == 2:
                # range(start, end)
                start, end = args
                for i in range(start, end):
                    # Assign loop variable to scope
                    self.global_scope[iterator_var] = i
                    # Execute loop body
                    try:
                        for statement in node.body:
                            self._evaluate_statement(statement)
                    except BreakSignal:
                        break  # Exit loop
                    except ContinueSignal:
                        continue  # Skip to next iteration
            elif len(args) == 3:
                # range(start, end, step)
                start, end, step = args
                for i in range(start, end, step):
                    # Assign loop variable to scope
                    self.global_scope[iterator_var] = i
                    # Execute loop body
                    try:
                        for statement in node.body:
                            self._evaluate_statement(statement)
                    except BreakSignal:
                        break  # Exit loop
                    except ContinueSignal:
                        continue  # Skip to next iteration
        else:
            # Generic iterator (simplified)
            iterator_var = node.iterator_var or 'item'
            iterable = self._evaluate_expression(node.condition_or_iter)
            if isinstance(iterable, (list, tuple, ArrObject)):
                for item in iterable:
                    # Assign loop variable to scope
                    self.global_scope[iterator_var] = item
                    try:
                        for statement in node.body:
                            self._evaluate_statement(statement)
                    except BreakSignal:
                        break  # Exit loop
                    except ContinueSignal:
                        continue  # Skip to next iteration
            elif isinstance(iterable, (dict, MapObject)):
                # Iterate over keys in insertion order
                keys = iterable.keys() if isinstance(iterable, MapObject) else list(iterable.keys())
                for key in keys:
                    # Assign loop variable to scope
                    self.global_scope[iterator_var] = key
                    try:
                        for statement in node.body:
                            self._evaluate_statement(statement)
                    except BreakSignal:
                        break  # Exit loop
                    except ContinueSignal:
                        continue  # Skip to next iteration
        
        return None
    
    def _evaluate_while_loop(self, node: LoopNode) -> Any:
        """Evaluate a while loop."""
        while self._is_truthy(self._evaluate_expression(node.condition_or_iter)):
            try:
                for statement in node.body:
                    self._evaluate_statement(statement)
            except BreakSignal:
                break  # Exit loop
            except ContinueSignal:
                continue  # Skip to next iteration
        return None
    
    def _evaluate_function_call(self, node: CallNode) -> Any:
        """Evaluate a function call."""
        if '.' in node.func_name:
            # Method call: obj.method() or obj.member.method()
            parts = node.func_name.split('.')
            obj_name = parts[0]
            member_path = parts[1:-1]  # All parts except the last one
            method_name = parts[-1]    # The last part is the method name
            
            if obj_name in self.global_scope:
                obj = self.global_scope[obj_name]
                
                # Navigate through the member path
                current_obj = obj
                for member_name in member_path:
                    if isinstance(current_obj, dict) and member_name in current_obj:
                        # Check if this is a class instance with access control
                        if '__instance_class__' in current_obj:
                            # Check attribute access
                            self._check_attribute_access(current_obj, member_name)
                        current_obj = current_obj[member_name]
                    elif hasattr(current_obj, '__getattr__'):
                        # Handle PyModuleProxy and similar objects
                        try:
                            current_obj = getattr(current_obj, member_name)
                        except AttributeError:
                            raise RuntimeErrorLyric(f"AttributeError: '{current_obj}' has no attribute '{member_name}'")
                    elif callable(current_obj):
                        # Handle classes and callable objects
                        try:
                            current_obj = getattr(current_obj, member_name)
                        except AttributeError:
                            raise RuntimeErrorLyric(f"AttributeError: '{current_obj}' has no attribute '{member_name}'")
                    else:
                        available_members = list(current_obj.keys()) if isinstance(current_obj, dict) else []
                        if available_members:
                            members_preview = ", ".join(available_members[:5])
                            if len(available_members) > 5:
                                members_preview += f" (and {len(available_members)-5} more)"
                            raise RuntimeErrorLyric(f"Member not found: '{member_name}' is not a member of '{current_obj}'. Available members: {members_preview}")
                        else:
                            raise RuntimeErrorLyric(f"Member not found: '{member_name}' is not a member of '{current_obj}'. '{current_obj}' is of type {type(current_obj).__name__} and has no members.")
                
                # Now get the method from the final object
                if isinstance(current_obj, dict) and method_name in current_obj:
                    method = current_obj[method_name]
                    if isinstance(method, dict) and 'params' in method and 'body' in method:
                        # It's a method definition - determine caller context for access control
                        caller_context = 'external'
                        if self.current_instance is not None:
                            # We're inside a method call
                            current_class = self.current_instance.get('__instance_class__')
                            target_class = current_obj.get('__instance_class__')
                            
                            # Check if calling from same instance (same class or derived)
                            if current_class == target_class:
                                caller_context = 'internal'
                            elif self._is_derived_from(current_class, target_class):
                                caller_context = 'derived'
                        
                        # Check access control
                        self._check_method_access(current_obj, method_name, method, caller_context)
                        
                        # Determine which class defines this method
                        defining_class = self._find_method_defining_class(current_obj, method_name)
                        
                        return self._call_method(current_obj, method, node.args, class_context=defining_class)
                    else:
                        # It's a regular attribute, call it if callable
                        args = [self._evaluate_expression(arg) for arg in node.args]
                        if callable(method):
                            return method(*args)
                        else:
                            raise RuntimeErrorLyric(f"Cannot call '{method_name}': it is not a function or method. '{method_name}' is of type {type(method).__name__}. Use parentheses () only for function calls.")
                elif hasattr(current_obj, '__getattr__'):
                    # Handle PyModuleProxy and similar objects
                    try:
                        method = getattr(current_obj, method_name)
                        args = [self._evaluate_expression(arg) for arg in node.args]
                        if callable(method):
                            return method(*args)
                        else:
                            raise RuntimeErrorLyric(f"Cannot call '{method_name}': it is not a function or method. '{method_name}' is of type {type(method).__name__}. Use parentheses () only for function calls.")
                    except AttributeError:
                        raise RuntimeErrorLyric(f"AttributeError: '{current_obj}' has no attribute '{method_name}'")
                elif isinstance(current_obj, RexMatch):
                    # Handle RexMatch methods
                    if hasattr(current_obj, method_name):
                        method = getattr(current_obj, method_name)
                        args = [self._evaluate_expression(arg) for arg in node.args]
                        if callable(method):
                            return method(*args)
                        else:
                            raise RuntimeErrorLyric(f"Cannot call '{method_name}': it is not a function or method. '{method_name}' is of type {type(method).__name__}. Use parentheses () only for function calls.")
                    else:
                        raise RuntimeErrorLyric(f"AttributeError: RexMatch has no attribute '{method_name}'")
                elif isinstance(current_obj, RexObject):
                    # Handle RexObject methods
                    if hasattr(current_obj, method_name):
                        method = getattr(current_obj, method_name)
                        args = [self._evaluate_expression(arg) for arg in node.args]
                        if callable(method):
                            return method(*args)
                        else:
                            raise RuntimeErrorLyric(f"Cannot call '{method_name}': it is not a function or method. '{method_name}' is of type {type(method).__name__}. Use parentheses () only for function calls.")
                    else:
                        raise RuntimeErrorLyric(f"AttributeError: RexObject has no attribute '{method_name}'")
                elif isinstance(current_obj, ArrObject):
                    # Handle ArrObject methods
                    if hasattr(current_obj, method_name):
                        method = getattr(current_obj, method_name)
                        args = [self._evaluate_expression(arg) for arg in node.args]
                        if callable(method):
                            return method(*args)
                        else:
                            raise RuntimeErrorLyric(f"Cannot call '{method_name}': it is not a function or method. '{method_name}' is of type {type(method).__name__}. Use parentheses () only for function calls.")
                    else:
                        raise RuntimeErrorLyric(f"AttributeError: ArrObject has no attribute '{method_name}'")
                elif isinstance(current_obj, MapObject):
                    # Handle MapObject methods
                    if hasattr(current_obj, method_name):
                        method = getattr(current_obj, method_name)
                        args = [self._evaluate_expression(arg) for arg in node.args]
                        if callable(method):
                            return method(*args)
                        else:
                            raise RuntimeErrorLyric(f"Cannot call '{method_name}': it is not a function or method. '{method_name}' is of type {type(method).__name__}. Use parentheses () only for function calls.")
                    else:
                        raise RuntimeErrorLyric(f"AttributeError: MapObject has no attribute '{method_name}'")
                elif isinstance(current_obj, DskObject):
                    # Handle DskObject methods
                    if hasattr(current_obj, method_name):
                        method = getattr(current_obj, method_name)
                        args = [self._evaluate_expression(arg) for arg in node.args]
                        if callable(method):
                            return method(*args)
                        else:
                            raise RuntimeErrorLyric(f"Cannot call '{method_name}': it is not a function or method. '{method_name}' is of type {type(method).__name__}. Use parentheses () only for function calls.")
                    else:
                        raise RuntimeErrorLyric(f"AttributeError: DskObject has no attribute '{method_name}'")
                elif callable(current_obj):
                    # Handle classes and callable objects
                    try:
                        method = getattr(current_obj, method_name)
                        args = [self._evaluate_expression(arg) for arg in node.args]
                        if callable(method):
                            return method(*args)
                        else:
                            raise RuntimeErrorLyric(f"Cannot call '{method_name}': it is not a function or method. '{method_name}' is of type {type(method).__name__}. Use parentheses () only for function calls.")
                    except AttributeError:
                        raise RuntimeErrorLyric(f"AttributeError: '{current_obj}' has no attribute '{method_name}'")
                else:
                    available_methods = [k for k, v in current_obj.items() if isinstance(v, dict) and 'params' in v and 'body' in v] if isinstance(current_obj, dict) else []
                    if available_methods:
                        methods_preview = ", ".join(available_methods[:5])
                        if len(available_methods) > 5:
                            methods_preview += f" (and {len(available_methods)-5} more)"
                        raise RuntimeErrorLyric(f"Method not found: '{method_name}' is not a method of '{current_obj}'. Available methods: {methods_preview}")
                    else:
                        raise RuntimeErrorLyric(f"Method not found: '{method_name}' is not a method of '{current_obj}'. '{current_obj}' is of type {type(current_obj).__name__} and has no methods.")
            else:
                raise RuntimeErrorLyric(f"Undefined variable: '{obj_name}' has not been declared. Use a type declaration (int, str, flt, var) or assign a value first")
        elif node.func_name == "print":
            # Built-in print function
            args = [self._evaluate_expression(arg) for arg in node.args]
            print(*args)
            return None
        elif node.func_name == "range":
            # Built-in range function - returns ArrObject for consistency with Lyric's arr type
            args = [self._evaluate_expression(arg) for arg in node.args]
            if len(args) == 1:
                return ArrObject(list(range(args[0])))
            elif len(args) == 2:
                return ArrObject(list(range(args[0], args[1])))
            elif len(args) == 3:
                return ArrObject(list(range(args[0], args[1], args[2])))
            else:
                raise RuntimeErrorLyric(f"Invalid range() arguments: range() takes 1-3 arguments (start, stop, step), but got {len(args)}. Usage: range(stop) or range(start, stop) or range(start, stop, step)")
        elif node.func_name in self.classes:
            # Class instantiation: ClassName()
            class_def = self.classes[node.func_name]
            
            # Create instance by copying from entire inheritance chain
            instance = {}
            
            # Helper function to recursively copy from inheritance chain
            def copy_from_inheritance_chain(class_name):
                """Recursively copy members from base classes up to root."""
                if class_name not in self.classes:
                    raise RuntimeErrorLyric(f"Class '{class_name}' is not defined")
                
                current_class_def = self.classes[class_name]
                
                # First, recursively copy from base class (if any)
                if '__base_class__' in current_class_def:
                    base_class_name = current_class_def['__base_class__']
                    copy_from_inheritance_chain(base_class_name)
                
                # Then copy this class's members (overriding base class members)
                for key, value in current_class_def.items():
                    if not key.startswith('__') or key == '__constructor__' or key.startswith('__visibility_'):
                        # Copy everything except __class_name__ and __base_class__
                        if key not in ('__class_name__', '__base_class__'):
                            instance[key] = value
            
            # Helper function to collect constructor chain from base to child
            def collect_constructor_chain(class_name):
                """Collect constructors in base→child order."""
                constructors = []
                
                if class_name not in self.classes:
                    return constructors
                
                current_class_def = self.classes[class_name]
                
                # First, recursively collect from base class (if any)
                if '__base_class__' in current_class_def:
                    base_class_name = current_class_def['__base_class__']
                    constructors.extend(collect_constructor_chain(base_class_name))
                
                # Then add this class's constructor (if it exists)
                if '__constructor__' in current_class_def:
                    constructors.append((class_name, current_class_def['__constructor__']))
                
                return constructors
            
            # Copy entire inheritance chain
            copy_from_inheritance_chain(node.func_name)
            
            # Add instance class name marker
            instance['__instance_class__'] = node.func_name
            
            # Store base class chain for method resolution
            if '__base_class__' in class_def:
                instance['__base_class__'] = class_def['__base_class__']
            
            # Call constructors in base→child order (automatic chaining)
            constructor_chain = collect_constructor_chain(node.func_name)
            for class_name, constructor_method in constructor_chain:
                # Only pass arguments to the most derived (child) constructor
                if class_name == node.func_name:
                    self._call_method(instance, constructor_method, node.args, class_context=class_name)
                else:
                    # Base class constructors are called with no arguments (automatic chaining)
                    self._call_method(instance, constructor_method, [], class_context=class_name)
            
            # Remove constructor from instance after calling all constructors
            if '__constructor__' in instance:
                del instance['__constructor__']
            
            # Also check for legacy init() method for backward compatibility (if no constructor was called)
            if not constructor_chain and 'init' in instance and isinstance(instance['init'], dict):
                init_method = instance['init']
                # Call the init method with the provided arguments
                self._call_method(instance, init_method, node.args)
            
            return instance
        elif node.func_name in self.global_scope and callable(self.global_scope[node.func_name]):
            # Built-in function from global scope
            args = [self._evaluate_expression(arg) for arg in node.args]
            return self.global_scope[node.func_name](*args)
        elif node.func_name in self.functions:
            # User-defined function
            args = [self._evaluate_expression(arg) for arg in node.args]
            return self._call_function(node.func_name, args)
        else:
            # Check if it might be a typo or suggest available functions
            available_functions = list(self.functions.keys())
            available_builtins = ['print', 'range', 'len', 'int', 'float', 'str', 'open', 'isinstance', 'type', 'regex', 'append', 'keys', 'values']
            all_available = available_functions + available_builtins
            
            # Find similar function names
            similar_functions = [f for f in all_available if f.startswith(node.func_name[:3])] if len(node.func_name) >= 3 else []
            
            if similar_functions:
                suggestions = ", ".join(similar_functions[:3])
                raise RuntimeErrorLyric(f"Function not found: '{node.func_name}' is not defined. Did you mean: {suggestions}? Available functions: {', '.join(available_functions[:5]) if available_functions else 'none defined'}")
            else:
                raise RuntimeErrorLyric(f"Function not found: '{node.func_name}' is not defined. Available functions: {', '.join(available_functions[:5]) if available_functions else 'none defined'}. Built-in functions: print, range, len, int, float, str")
    
    def _evaluate_expression(self, expr) -> Any:
        """Evaluate an expression."""
        if isinstance(expr, LiteralNode):
            return expr.value
        elif isinstance(expr, IdentifierNode):
            return self._evaluate_identifier(expr)
        elif isinstance(expr, BinaryOpNode):
            return self._evaluate_binary_operation(expr)
        elif isinstance(expr, UnaryOpNode):
            return self._evaluate_unary_operation(expr)
        elif isinstance(expr, CallNode):
            return self._evaluate_function_call(expr)
        elif isinstance(expr, ListLiteralNode):
            return self._evaluate_list_literal(expr)
        elif isinstance(expr, DictLiteralNode):
            return self._evaluate_dict_literal(expr)
        elif isinstance(expr, IndexNode):
            return self._evaluate_index(expr)
        elif isinstance(expr, SliceNode):
            return self._evaluate_slice(expr)
        elif isinstance(expr, RexNode):
            return self._evaluate_rex_literal(expr)
        else:
            raise RuntimeErrorLyric(f"Unknown expression type: {type(expr)}")
    
    def _evaluate_identifier(self, node: IdentifierNode) -> Any:
        """Evaluate an identifier."""
        if '.' in node.name:
            # Member access: obj.member or obj.member.member
            parts = node.name.split('.')
            obj_name = parts[0]
            member_path = parts[1:]
            
            if obj_name in self.global_scope:
                obj = self.global_scope[obj_name]
                
                # Navigate through the member path
                current_obj = obj
                for member_name in member_path:
                    if isinstance(current_obj, dict) and member_name in current_obj:
                        # Check if this is a class instance with access control
                        if '__instance_class__' in current_obj:
                            # Check attribute access
                            self._check_attribute_access(current_obj, member_name)
                        current_obj = current_obj[member_name]
                    elif hasattr(current_obj, '__getattr__'):
                        # Handle PyModuleProxy and similar objects
                        try:
                            current_obj = getattr(current_obj, member_name)
                        except AttributeError:
                            raise RuntimeErrorLyric(f"AttributeError: '{current_obj}' has no attribute '{member_name}'")
                    elif hasattr(current_obj, member_name):
                        # Handle Python objects with attributes
                        try:
                            current_obj = getattr(current_obj, member_name)
                        except AttributeError:
                            raise RuntimeErrorLyric(f"AttributeError: '{current_obj}' has no attribute '{member_name}'")
                    else:
                        available_members = list(current_obj.keys()) if isinstance(current_obj, dict) else []
                        if available_members:
                            members_preview = ", ".join(available_members[:5])
                            if len(available_members) > 5:
                                members_preview += f" (and {len(available_members)-5} more)"
                            raise RuntimeErrorLyric(f"Member not found: '{member_name}' is not a member of '{current_obj}'. Available members: {members_preview}")
                        else:
                            raise RuntimeErrorLyric(f"Member not found: '{member_name}' is not a member of '{current_obj}'. '{current_obj}' is of type {type(current_obj).__name__} and has no members.")
                
                return current_obj
            else:
                raise RuntimeErrorLyric(f"Undefined variable: '{obj_name}' has not been declared. Use a type declaration (int, str, flt, var) or assign a value first")
        else:
            # Simple identifier
            if node.name in self.global_scope:
                return self.global_scope[node.name]
            elif node.name in self.classes:
                # Class reference - return the class definition
                return self.classes[node.name]
            else:
                # Check if it might be a typo or suggest available variables
                available_vars = list(self.global_scope.keys())
                available_classes = list(self.classes.keys())
                
                if available_vars or available_classes:
                    suggestions = []
                    if available_vars:
                        suggestions.append(f"variables: {', '.join(available_vars[:3])}")
                    if available_classes:
                        suggestions.append(f"classes: {', '.join(available_classes[:3])}")
                    suggestions_str = ", ".join(suggestions)
                    raise RuntimeErrorLyric(f"Undefined variable: '{node.name}' has not been declared. Available {suggestions_str}. Use a type declaration (int, str, flt, var) or assign a value first")
                else:
                    raise RuntimeErrorLyric(f"Undefined variable: '{node.name}' has not been declared. No variables are defined yet. Use a type declaration (int, str, flt, var) or assign a value first")
    
    def _evaluate_binary_operation(self, node: BinaryOpNode) -> Any:
        """Evaluate a binary operation."""
        left = self._evaluate_expression(node.left)
        right = self._evaluate_expression(node.right)
        
        try:
            if node.op == '+':
                # Handle string concatenation with mixed types
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            elif node.op == '-':
                return left - right
            elif node.op == '*':
                return left * right
            elif node.op == '/':
                if right == 0:
                    raise RuntimeErrorLyric("Division by zero: cannot divide by zero. Check your divisor value before performing division.", node.line, node.column)
                return left / right
            elif node.op == '==':
                return left == right
            elif node.op == '!=':
                return left != right
            elif node.op == '<':
                return left < right
            elif node.op == '<=':
                return left <= right
            elif node.op == '>':
                return left > right
            elif node.op == '>=':
                return left >= right
            elif node.op == 'and':
                return self._is_truthy(left) and self._is_truthy(right)
            elif node.op == 'or':
                return self._is_truthy(left) or self._is_truthy(right)
            elif node.op == 'in':
                # Membership check: key in dict, item in list, char in string
                if isinstance(right, MapObject):
                    return left in right  # MapObject implements __contains__
                elif isinstance(right, (dict, list, str, tuple, ArrObject)):
                    return left in right
                else:
                    raise TypeErrorLyric(f"'in' requires a container (map, arr, str), got {type(right).__name__}")
            else:
                raise RuntimeErrorLyric(f"Unknown binary operator: {node.op}", node.line, node.column)
        except TypeError as e:
            raise RuntimeErrorLyric(f"Type mismatch in operation '{node.op}': {str(e)}. Check that both operands are compatible types for this operation.", node.line, node.column)
    
    def _evaluate_unary_operation(self, node: UnaryOpNode) -> Any:
        """Evaluate a unary operation."""
        operand = self._evaluate_expression(node.operand)
        
        if node.op == '-':
            return -operand
        elif node.op == '!' or node.op == 'not':
            return not self._is_truthy(operand)
        else:
            raise RuntimeErrorLyric(f"Unknown unary operator: '{node.op}'. Supported unary operators are: -, !, not")
    
    def _evaluate_try_statement(self, node: TryNode) -> Any:
        """Evaluate a try/catch/finally statement with typed exception binding."""
        result = None
        exception_occurred = None
        
        try:
            # Execute try body
            for statement in node.try_body:
                result = self._evaluate_statement(statement)
                if isinstance(result, ReturnValue):
                    # Store result but don't return yet - finally must execute
                    result = result
                    break
        except Exception as e:
            # Convert Python exceptions to Lyric exceptions (check Python types first!)
            if isinstance(e, IndexError) and not isinstance(e, IndexErrorLyric):
                e = IndexErrorLyric(str(e))
            elif isinstance(e, KeyError) and not isinstance(e, KeyErrorLyric):
                e = KeyErrorLyric(str(e))
            elif isinstance(e, TypeError) and not isinstance(e, TypeErrorLyric):
                e = TypeErrorLyric(str(e))
            elif isinstance(e, ValueError) and not isinstance(e, ValueErrorLyric):
                e = ValueErrorLyric(str(e))
            elif isinstance(e, AttributeError) and not isinstance(e, AttributeErrorLyric):
                e = AttributeErrorLyric(str(e))
            elif isinstance(e, ZeroDivisionError) and not isinstance(e, ZeroDivisionErrorLyric):
                e = ZeroDivisionErrorLyric(str(e))
            # Catch any exception that occurs
            exception_occurred = e
        
        # If an exception occurred, try to match it with catch clauses
        if exception_occurred and node.catch_clauses:
            matched_clause = None
            
            # Find the first matching catch clause
            for catch_clause in node.catch_clauses:
                if self._exception_matches_clause(exception_occurred, catch_clause):
                    matched_clause = catch_clause
                    break
            
            # Execute the matching catch clause
            if matched_clause:
                # Bind exception to variable if specified
                if matched_clause.variable_name:
                    self.global_scope[matched_clause.variable_name] = exception_occurred
                
                # Execute catch body
                for statement in matched_clause.body:
                    result = self._evaluate_statement(statement)
                    if isinstance(result, ReturnValue):
                        # Store result but don't return yet - finally must execute
                        result = result
                        break
                
                # Clear the exception since it was caught
                exception_occurred = None
        
        # Execute finally block if it exists (always executes)
        if node.finally_body:
            for statement in node.finally_body:
                finally_result = self._evaluate_statement(statement)
                if isinstance(finally_result, ReturnValue):
                    # Finally block return takes precedence
                    result = finally_result
        
        # If exception was not caught, re-raise it
        if exception_occurred:
            raise exception_occurred
        
        # Return the result (could be from try, catch, or finally)
        if isinstance(result, ReturnValue):
            return result
        
        return None
    
    def _exception_matches_clause(self, exception: Exception, catch_clause: CatchClauseNode) -> bool:
        """Check if an exception matches a catch clause based on type."""
        if catch_clause.exception_type is None:
            # Bare catch clause matches all exceptions
            return True
        
        # Get the exception type class
        exception_type_class = EXCEPTION_TYPES.get(catch_clause.exception_type)
        if exception_type_class is None:
            # Unknown exception type - treat as bare catch
            return True
        
        # Check if the exception is an instance of the specified type
        return isinstance(exception, exception_type_class)
    
    def _evaluate_raise_statement(self, node: RaiseNode) -> None:
        """Evaluate a raise statement."""
        exception_name = node.exception_name
        
        # Map exception names to Python exceptions
        # Support both Lyric-style names (with Lyric suffix) and standard Python names
        exception_map = {
            'RuntimeErrorLyric': RuntimeErrorLyric,
            'IndexErrorLyric': IndexError,
            'TypeErrorLyric': TypeError,
            'ValueErrorLyric': ValueError,
            'KeyErrorLyric': KeyError,
            'AttributeErrorLyric': AttributeError,
            'ZeroDivisionErrorLyric': ZeroDivisionError,
            'RuntimeError': RuntimeErrorLyric,  # Map RuntimeError to RuntimeErrorLyric
            'IndexError': IndexError,
            'TypeError': TypeError,
            'ValueError': ValueError,
            'KeyError': KeyError,
            'AttributeError': AttributeError,
            'ZeroDivisionError': ZeroDivisionError,
        }
        
        if exception_name in exception_map:
            raise exception_map[exception_name](f"{exception_name} raised")
        else:
            # Default to RuntimeErrorLyric for unknown exceptions
            available_exceptions = list(exception_map.keys())
            raise RuntimeErrorLyric(f"Unknown exception: '{exception_name}' is not a valid exception type. Available exceptions: {', '.join(available_exceptions[:5])} (and more)")
    
    def _evaluate_import_statement(self, node: ImportNode) -> None:
        """Evaluate an import statement for Lyric modules."""
        import os
        from lyric.lexer import tokenize
        from lyric.parser import Parser
        
        module_name = node.module_name
        
        # Search for the module in the following order:
        # 1. Current working directory
        # 2. Directory of the script being executed (if known)
        # 3. LYRIC_PATH environment variable
        
        search_paths = [
            os.getcwd(),  # Current working directory
        ]
        
        # Add the directory of the source file if known
        if self.source_file:
            source_dir = os.path.dirname(os.path.abspath(self.source_file))
            if source_dir not in search_paths:
                search_paths.append(source_dir)
        
        # Add LYRIC_PATH if set
        lyric_path = os.environ.get('LYRIC_PATH', '')
        if lyric_path:
            search_paths.extend(lyric_path.split(os.pathsep))
        
        # Try to find the module file
        module_file = None
        for search_path in search_paths:
            # Try .ly extension
            candidate = os.path.join(search_path, f"{module_name}.ly")
            if os.path.isfile(candidate):
                module_file = candidate
                break
            
            # Try as a directory with __init__.ly
            candidate_init = os.path.join(search_path, module_name, "__init__.ly")
            if os.path.isfile(candidate_init):
                module_file = candidate_init
                break
        
        if module_file is None:
            raise RuntimeErrorLyric(
                f"ModuleNotFoundError: No module named '{module_name}'. "
                f"Searched in: {', '.join(search_paths)}",
                node.line,
                node.column
            )
        
        # Read and parse the module
        try:
            with open(module_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
        except Exception as e:
            raise RuntimeErrorLyric(
                f"Error reading module '{module_name}' from '{module_file}': {e}",
                node.line,
                node.column
            )
        
        # Parse the module
        try:
            tokens = tokenize(source_code)
            parser = Parser(tokens)
            module_ast = parser.parse()
        except Exception as e:
            raise RuntimeErrorLyric(
                f"Error parsing module '{module_name}': {e}",
                node.line,
                node.column
            )
        
        # Create a new interpreter for the module with its own scope
        module_interpreter = Interpreter()
        
        # Evaluate the module
        try:
            module_interpreter.evaluate(module_ast)
        except Exception as e:
            raise RuntimeErrorLyric(
                f"Error executing module '{module_name}': {e}",
                node.line,
                node.column
            )
        
        # Import functions, classes, and module-level variables from the module
        # However, functions need to retain access to their module's global scope
        
        if node.symbols:
            # Selective import: import module; symbol1, symbol2
            for symbol_name, alias in node.symbols:
                # Check if it's a function
                if symbol_name in module_interpreter.functions:
                    func = module_interpreter.functions[symbol_name]
                    func_with_scope = func.copy()
                    func_with_scope['module_scope'] = module_interpreter.global_scope
                    
                    # Use alias if provided, otherwise use original name
                    target_name = alias if alias else symbol_name
                    self.functions[target_name] = func_with_scope
                
                # Check if it's a class
                elif symbol_name in module_interpreter.classes:
                    cls = module_interpreter.classes[symbol_name]
                    
                    # Classes are imported into the classes dict
                    # Aliases are not supported for classes - user should use var alias = ClassName()
                    if alias:
                        raise RuntimeErrorLyric(
                            f"ImportError: 'as' keyword is not supported for class imports. "
                            f"To create an alias for '{symbol_name}', use: var {alias} = {symbol_name}() after importing.",
                            node.line,
                            node.column
                        )
                    
                    self.classes[symbol_name] = cls
                
                # Check if it's a module-level variable
                elif symbol_name in module_interpreter.global_scope:
                    value = module_interpreter.global_scope[symbol_name]
                    
                    # Use alias if provided, otherwise use original name
                    target_name = alias if alias else symbol_name
                    self.global_scope[target_name] = value
                
                # Symbol not found
                else:
                    raise RuntimeErrorLyric(
                        f"ImportError: cannot import name '{symbol_name}' from module '{module_name}'. "
                        f"'{symbol_name}' is not defined in the module.",
                        node.line,
                        node.column
                    )
        else:
            # Import all functions, classes, and variables from the module
            
            # Import functions with their module scope
            for name, func in module_interpreter.functions.items():
                # Attach module scope to function so it can access module variables
                func_with_scope = func.copy()
                func_with_scope['module_scope'] = module_interpreter.global_scope
                self.functions[name] = func_with_scope
            
            # Import classes
            for name, cls in module_interpreter.classes.items():
                self.classes[name] = cls
            
            # Import module-level variables
            # We need to filter out built-in functions and only import user-defined variables
            for name, value in module_interpreter.global_scope.items():
                # Skip built-in functions (they are callables)
                if not callable(value):
                    self.global_scope[name] = value
        
        return None
    
    def _evaluate_importpy_statement(self, node: ImportPyNode) -> None:
        """Evaluate an importpy statement."""
        from lyric.pyproxy import PyModuleProxy
        
        # Create the module proxy and bind it to the global scope
        proxy = PyModuleProxy(node.module_name)
        self.global_scope[node.module_name] = proxy
        
        return None
    
    def _evaluate_file_op(self, node: FileOpNode) -> None:
        """Evaluate a file operator statement: expr ->> dsk, expr -> dsk, or expr <- dsk"""
        left_val = self._evaluate_expression(node.left)
        right_val = self._evaluate_expression(node.right)
        
        if node.operator in ('->>', '->'):
            # Write operations: right side must be dsk
            if not isinstance(right_val, DskObject):
                raise RuntimeErrorLyric(
                    f"File write operators ({node.operator}) require dsk type on right side, got {type(right_val).__name__}",
                    node.line, node.column
                )
            
            if node.operator == '->>':
                # Append operation
                if isinstance(left_val, str):
                    # Append string to file
                    right_val.append(left_val)
                elif isinstance(left_val, ArrObject):
                    # Append array elements as lines
                    for item in left_val.elements:
                        right_val.append(str(item) + '\n')
                elif isinstance(left_val, (int, float, bool)):
                    # Append primitive value as string
                    right_val.append(str(left_val) + '\n')
                elif isinstance(left_val, MapObject):
                    # Append map as JSON-like string
                    right_val.append(str(left_val.elements) + '\n')
                else:
                    raise RuntimeErrorLyric(
                        f"Cannot append {type(left_val).__name__} to file. Supported types: str, arr, int, flt, god, map",
                        node.line, node.column
                    )
            else:  # node.operator == '->'
                # Overwrite operation
                if isinstance(left_val, str):
                    # Overwrite file with string
                    right_val.overwrite(left_val)
                elif isinstance(left_val, ArrObject):
                    # Overwrite file with array elements as lines
                    content = '\n'.join(str(item) for item in left_val.elements)
                    right_val.overwrite(content)
                elif isinstance(left_val, (int, float, bool)):
                    # Overwrite with primitive value
                    right_val.overwrite(str(left_val))
                elif isinstance(left_val, MapObject):
                    # Overwrite with map as JSON-like string
                    right_val.overwrite(str(left_val.elements))
                else:
                    raise RuntimeErrorLyric(
                        f"Cannot write {type(left_val).__name__} to file. Supported types: str, arr, int, flt, god, map",
                        node.line, node.column
                    )
        
        elif node.operator == '<-':
            # Read operation: right side must be dsk, left side must be a variable identifier
            if not isinstance(right_val, DskObject):
                raise RuntimeErrorLyric(
                    f"File read operator (<-) requires dsk type on right side, got {type(right_val).__name__}",
                    node.line, node.column
                )
            
            # Left side must be an identifier (variable name)
            if not isinstance(node.left, IdentifierNode):
                raise RuntimeErrorLyric(
                    f"File read operator (<-) requires variable name on left side, not expression",
                    node.line, node.column
                )
            
            var_name = node.left.name
            
            # Get the declared type of the variable if it exists
            var_type = self._get_variable_type(var_name)
            
            # Read from file
            if var_type == 'arr' or (var_type == 'var' and isinstance(self.global_scope.get(var_name), ArrObject)):
                # Read file as array of lines
                content = right_val.read()
                lines = content.splitlines()
                self.global_scope[var_name] = ArrObject(lines)
            else:
                # Read file as string (default)
                content = right_val.read()
                self.global_scope[var_name] = content
        
        else:
            raise RuntimeErrorLyric(
                f"Unknown file operator: {node.operator}",
                node.line, node.column
            )
        
        return None
    
    def _evaluate_return_statement(self, node: ReturnNode) -> ReturnValue:
        """Evaluate a return statement."""
        if node.value is not None:
            value = self._evaluate_expression(node.value)
        else:
            value = None
        return ReturnValue(value)
    
    def _evaluate_break_statement(self, node: BreakNode) -> None:
        """Evaluate a break statement."""
        # Raise BreakSignal to exit the enclosing loop
        raise BreakSignal(node.line, node.column)
    
    def _evaluate_continue_statement(self, node: ContinueNode) -> None:
        """Evaluate a continue statement."""
        # Raise ContinueSignal to skip to next iteration of the enclosing loop
        raise ContinueSignal(node.line, node.column)
    
    def _is_truthy(self, value: Any) -> bool:
        """Check if a value is truthy."""
        if value is None:
            return False
        elif isinstance(value, bool):
            return value
        elif isinstance(value, (int, float)):
            return value != 0
        elif isinstance(value, str):
            return len(value) > 0
        elif isinstance(value, (list, tuple)):
            return len(value) > 0
        else:
            return True


def evaluate(ast: ProgramNode, source_file=None, cli_args=None) -> Any:
    """Evaluate an AST and return the result.
    
    Args:
        ast: The program AST to evaluate
        source_file: Optional path to the source file (for relative imports)
        cli_args: Optional list of command-line arguments to pass to main()
    """
    interpreter = Interpreter(source_file=source_file)
    if cli_args:
        interpreter.cli_args = cli_args
    return interpreter.evaluate(ast)