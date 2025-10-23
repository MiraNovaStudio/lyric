"""Interpreter module for executing Lyric AST nodes."""

from typing import Any, List
import re
from lyric.ast_nodes import (
    ProgramNode, FunctionNode, IfNode, LoopNode, AssignNode, CallNode,
    BinaryOpNode, UnaryOpNode, LiteralNode, IdentifierNode, ClassNode, ReturnNode, 
    ListLiteralNode, DictLiteralNode, IndexNode, TypeDeclarationNode, MultiDeclarationNode, TryNode, RaiseNode, ImportPyNode, RexNode
)
from lyric.errors import RuntimeErrorLyric
from lyric.runtime import register_builtins


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
    
    # TODO: Future enhancement - .search() method for mid-string matches
    # def search(self, text: str) -> bool:
    #     """Search for the regex pattern anywhere in the text (not just at the beginning)."""
    #     # Implementation would use Python's re.search() instead of re.match()
    #     # This method is deferred for future sprints to keep the initial rex implementation focused
    
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
        # Track variable types
        self.variable_types = {}
        # Register built-in functions
        register_builtins(self.global_scope)
        self.functions = {}
        self.classes = {}
    
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
            raise RuntimeErrorLyric(f"Runtime error: {str(e)}")
    
    def _call_function(self, func_name: str, args: List[Any]) -> Any:
        """Call a function by name with arguments."""
        if func_name in self.functions:
            func_def = self.functions[func_name]
            params = func_def['params']
            param_types = func_def.get('param_types', [])
            body = func_def['body']
            
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
            
            # Set local scope
            self.global_scope.update(local_scope)
            
            try:
                # Execute function body
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
        elif isinstance(statement, TryNode):
            return self._evaluate_try_statement(statement)
        elif isinstance(statement, RaiseNode):
            return self._evaluate_raise_statement(statement)
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
                            raise RuntimeErrorLyric(f"Index out of range: tried to access index {index} in list of length {len(obj)}. Valid indices are 0 to {len(obj)-1}", node.line, node.column)
                        obj[index] = value
                    except ValueError:
                        raise RuntimeErrorLyric(f"Invalid list index: '{index_str}' is not a valid integer. List indices must be integers.", node.line, node.column)
                else:
                    raise RuntimeErrorLyric(f"Cannot assign to indexed expression: '{obj_name}' is of type {type(obj).__name__}, but only lists and dictionaries support indexed assignment", node.line, node.column)
            else:
                raise RuntimeErrorLyric(f"Undefined variable: '{obj_name}' has not been declared. Use a type declaration (int, str, flt, var) or assign a value first", node.line, node.column)
        else:
            # Regular assignment
            # Check type enforcement if variable was declared with a type
            if node.name in self.variable_types:
                expected_type = self.variable_types[node.name]
                if expected_type != 'var' and not self._is_type_compatible(expected_type, value):
                    raise RuntimeErrorLyric(
                        f"Type mismatch: cannot assign {type(value).__name__} to variable '{node.name}' declared as {expected_type}. "
                        f"Expected {expected_type}, but got {type(value).__name__}. "
                        f"Use 'var {node.name} = ...' if you need dynamic typing.",
                        node.line, node.column
                    )
            
            self.global_scope[node.name] = value
        
        return value
    
    def _evaluate_type_declaration(self, node: TypeDeclarationNode) -> Any:
        """Evaluate a type declaration statement."""
        value = self._evaluate_expression(node.expr)
        
        # Store the variable type
        self.variable_types[node.name] = node.type_name
        
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
        # Declare all variables as uninitialized
        for type_name, var_name in node.declarations:
            # Store the variable type
            self.variable_types[var_name] = type_name
            
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
                raise RuntimeErrorLyric(f"Invalid list index: expected integer, but got {type(index).__name__}. List indices must be integers (0, 1, 2, ...)")
            if index < 0 or index >= len(obj):
                raise RuntimeErrorLyric(f"Index out of range: tried to access index {index} in list of length {len(obj)}. Valid indices are 0 to {len(obj)-1}")
            return obj[index]
        elif isinstance(obj, dict):
            if index not in obj:
                available_keys = list(obj.keys())[:5]  # Show first 5 keys
                keys_preview = ", ".join(repr(k) for k in available_keys)
                if len(obj) > 5:
                    keys_preview += f" (and {len(obj)-5} more)"
                raise RuntimeErrorLyric(f"Key not found: '{index}' is not a key in this dictionary. Available keys: {keys_preview}")
            return obj[index]
        else:
            raise RuntimeErrorLyric(f"Cannot index object: '{type(obj).__name__}' does not support indexing. Only lists and dictionaries can be indexed with []. Use dot notation (.) for object properties.")
    
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
        self.functions[node.name] = {
            'params': node.params,
            'param_types': node.param_types,
            'body': node.body_statements
        }
    
    def _evaluate_class_definition(self, node: ClassNode) -> None:
        """Evaluate a class definition."""
        class_dict = {}
        # Add a special marker to identify this as a class definition
        class_dict['__class_name__'] = node.name
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
                    for statement in node.body:
                        self._evaluate_statement(statement)
            elif len(args) == 2:
                # range(start, end)
                start, end = args
                for i in range(start, end):
                    # Assign loop variable to scope
                    self.global_scope[iterator_var] = i
                    # Execute loop body
                    for statement in node.body:
                        self._evaluate_statement(statement)
            elif len(args) == 3:
                # range(start, end, step)
                start, end, step = args
                for i in range(start, end, step):
                    # Assign loop variable to scope
                    self.global_scope[iterator_var] = i
                    # Execute loop body
                    for statement in node.body:
                        self._evaluate_statement(statement)
        else:
            # Generic iterator (simplified)
            iterable = self._evaluate_expression(node.condition_or_iter)
            if isinstance(iterable, (list, tuple)):
                for item in iterable:
                    for statement in node.body:
                        self._evaluate_statement(statement)
        
        return None
    
    def _evaluate_while_loop(self, node: LoopNode) -> Any:
        """Evaluate a while loop."""
        while self._is_truthy(self._evaluate_expression(node.condition_or_iter)):
            for statement in node.body:
                self._evaluate_statement(statement)
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
            
            # Check if class has an init() method and call it
            if 'init' in instance and isinstance(instance['init'], dict):
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
            available_builtins = ['print', 'range', 'len', 'int', 'float', 'str', 'open', 'isinstance', 'type', 'append', 'keys', 'values']
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
                return left + right
            elif node.op == '-':
                return left - right
            elif node.op == '*':
                return left * right
            elif node.op == '/':
                if right == 0:
                    raise RuntimeErrorLyric("Division by zero: cannot divide by zero. Check your divisor value before performing division.")
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
                raise RuntimeErrorLyric(f"Unknown binary operator: {node.op}")
        except TypeError as e:
            raise RuntimeErrorLyric(f"Type mismatch in operation '{node.op}': {str(e)}. Check that both operands are compatible types for this operation.")
    
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
        """Evaluate a try/catch/finally statement."""
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
            # Catch any exception that occurs
            exception_occurred = e
        
        # If an exception occurred and there's a catch block, execute it
        if exception_occurred and node.catch_body:
            for statement in node.catch_body:
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
    
    def _evaluate_importpy_statement(self, node: ImportPyNode) -> None:
        """Evaluate an importpy statement."""
        from lyric.pyproxy import PyModuleProxy
        
        # Create the module proxy and bind it to the global scope
        proxy = PyModuleProxy(node.module_name)
        self.global_scope[node.module_name] = proxy
        
        return None
    
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