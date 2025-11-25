# Lyric Programming Language
# Copyright (c) 2025 MiraNova Studios
# Designed and Architected by Michael (Aeonath) and ChatGPT
# Implemented by Claude
# Licensed under the MIT License with Source Attribution

"""Interpreter module for executing Lyric AST nodes."""

from typing import Any, List
import re
from lyric.ast_nodes import (
    ProgramNode, FunctionNode, IfNode, LoopNode, AssignNode, CallNode,
    BinaryOpNode, UnaryOpNode, LiteralNode, IdentifierNode, ClassNode, ReturnNode, BreakNode, ContinueNode,
    ListLiteralNode, DictLiteralNode, IndexNode, SliceNode, TypeDeclarationNode, MultiDeclarationNode, TryNode, CatchClauseNode, RaiseNode, ImportNode, ImportPyNode, RexNode
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


class ReturnValue:
    """Wrapper for return values to distinguish them from normal expression values."""
    def __init__(self, value):
        self.value = value


class Interpreter:
    """Interpreter for executing Lyric AST nodes."""
    
    def __init__(self):
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
                return self._call_function("main", [])
            
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
    
    def _call_method(self, instance: dict, method: dict, args: List[Any]) -> Any:
        """Call a method on an instance."""
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
        
        # Save current scope
        old_scope = self.global_scope.copy()
        
        # Set local scope
        self.global_scope.update(local_scope)
        
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
            # Restore scope
            self.global_scope = old_scope
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
                if isinstance(obj, dict):
                    # For dictionaries, the index is a key
                    obj[index_str] = value
                elif isinstance(obj, list):
                    # For lists, the index should be an integer
                    try:
                        index = int(index_str)
                        if index < 0 or index >= len(obj):
                            raise IndexErrorLyric(f"Index out of range: tried to access index {index} in list of length {len(obj)}. Valid indices are 0 to {len(obj)-1}", node.line, node.column)
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
            return isinstance(value, list)  # arr maps to Python list
        elif expected_type == 'map':
            return isinstance(value, dict)  # map maps to Python dict
        else:
            return False
    
    def _evaluate_return_statement(self, node: ReturnNode) -> ReturnValue:
        """Evaluate a return statement."""
        if node.value:
            return ReturnValue(self._evaluate_expression(node.value))
        return ReturnValue(None)
    
    def _evaluate_list_literal(self, node: ListLiteralNode) -> List[Any]:
        """Evaluate a list literal."""
        return [self._evaluate_expression(elem) for elem in node.elements]
    
    def _evaluate_dict_literal(self, node: DictLiteralNode) -> dict:
        """Evaluate a dictionary literal."""
        result = {}
        for key_expr, value_expr in node.pairs:
            key = self._evaluate_expression(key_expr)
            value = self._evaluate_expression(value_expr)
            result[key] = value
        return result
    
    def _evaluate_index(self, node: IndexNode) -> Any:
        """Evaluate an indexing operation."""
        obj = self._evaluate_expression(node.obj)
        index = self._evaluate_expression(node.index)
        
        if isinstance(obj, (list, tuple)):
            if not isinstance(index, int):
                raise TypeErrorLyric(f"Invalid list index: expected integer, but got {type(index).__name__}. List indices must be integers (0, 1, 2, ...)")
            if index < 0 or index >= len(obj):
                raise IndexErrorLyric(f"Index out of range: tried to access index {index} in list of length {len(obj)}. Valid indices are 0 to {len(obj)-1}")
            return obj[index]
        elif isinstance(obj, dict):
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
        
        # Store constructor method separately if it exists
        if node.constructor_method:
            class_dict['__constructor__'] = {
                'params': node.constructor_method.params,
                'param_types': node.constructor_method.param_types,
                'body': node.constructor_method.body_statements
            }
        
        for member in node.members_statements:
            if isinstance(member, AssignNode):
                # Class member assignment
                value = self._evaluate_expression(member.expr)
                class_dict[member.name] = value
            elif isinstance(member, MultiDeclarationNode):
                # Multi-variable declaration in class
                for type_name, var_name in member.declarations:
                    class_dict[var_name] = None  # Declare as uninitialized
            elif isinstance(member, FunctionNode):
                # Class method
                class_dict[member.name] = {
                    'params': member.params,
                    'param_types': member.param_types,
                    'body': member.body_statements
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
            if isinstance(iterable, (list, tuple)):
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
                        # It's a method definition
                        return self._call_method(current_obj, method, node.args)
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
            # Built-in range function
            args = [self._evaluate_expression(arg) for arg in node.args]
            if len(args) == 1:
                return list(range(args[0]))
            elif len(args) == 2:
                return list(range(args[0], args[1]))
            elif len(args) == 3:
                return list(range(args[0], args[1], args[2]))
            else:
                raise RuntimeErrorLyric(f"Invalid range() arguments: range() takes 1-3 arguments (start, stop, step), but got {len(args)}. Usage: range(stop) or range(start, stop) or range(start, stop, step)")
        elif node.func_name in self.classes:
            # Class instantiation: ClassName()
            class_def = self.classes[node.func_name]
            # Create instance as a copy of class definition
            instance = dict(class_def)
            # Add instance class name marker
            instance['__instance_class__'] = node.func_name
            
            # Check if class has a constructor method (method name matches class name)
            if '__constructor__' in instance and isinstance(instance['__constructor__'], dict):
                constructor_method = instance['__constructor__']
                # Call the constructor method with the provided arguments
                self._call_method(instance, constructor_method, node.args)
            # Also check for legacy init() method for backward compatibility
            elif 'init' in instance and isinstance(instance['init'], dict):
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
        # 1. Current directory
        # 2. LYRIC_PATH environment variable
        # 3. Standard library location (if it exists)
        
        search_paths = [
            os.getcwd(),  # Current directory
        ]
        
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
        
        # Import ONLY functions and classes from the module
        # Variables (including arrays, maps, etc.) are NOT imported
        # However, functions need to retain access to their module's global scope
        
        # Import functions with their module scope
        for name, func in module_interpreter.functions.items():
            # Attach module scope to function so it can access module variables
            func_with_scope = func.copy()
            func_with_scope['module_scope'] = module_interpreter.global_scope
            self.functions[name] = func_with_scope
        
        # Import classes
        for name, cls in module_interpreter.classes.items():
            self.classes[name] = cls
        
        return None
    
    def _evaluate_importpy_statement(self, node: ImportPyNode) -> None:
        """Evaluate an importpy statement."""
        from lyric.pyproxy import PyModuleProxy
        
        # Create the module proxy and bind it to the global scope
        proxy = PyModuleProxy(node.module_name)
        self.global_scope[node.module_name] = proxy
        
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


def evaluate(ast: ProgramNode) -> Any:
    """Evaluate an AST and return the result."""
    interpreter = Interpreter()
    return interpreter.evaluate(ast)