"""
Interpreter module for the Lyric language.
Executes AST nodes to run programs.
"""

from typing import Dict, List, Any, Optional
from lyric.ast import (
    ProgramNode, FunctionNode, ClassNode, IfNode, LoopNode,
    AssignNode, CallNode, BinaryOpNode, UnaryOpNode, LiteralNode,
    IdentifierNode, PrintNode, ImportNode, ReturnNode, MemberAccessNode, MethodCallNode, IndexNode
)
from lyric.errors import RuntimeErrorLyric, StackFrame
from lyric.runtime import register_builtins, BuiltinFunction


class Environment:
    """Represents a local environment (scope) for variable storage."""

    def __init__(self, parent: Optional['Environment'] = None, interpreter: Optional['Interpreter'] = None):
        self.variables: Dict[str, Any] = {}
        self.variable_types: Dict[str, str] = {}  # Track variable types
        self.parent = parent
        self.interpreter = interpreter
        self._cache: Dict[str, Any] = {}  # Cache for variable lookups
        self._cache_valid = True  # Cache validity flag

    def define(self, name: str, value: Any, type_annotation: Optional[str] = None) -> None:
        """Define a variable in this environment with optional type annotation."""
        # Type inference for literals if no type annotation provided
        if type_annotation is None:
            if isinstance(value, bool):
                type_annotation = 'bool'
            elif isinstance(value, int):
                type_annotation = 'int'
            elif isinstance(value, float):
                type_annotation = 'float'
            elif isinstance(value, str):
                type_annotation = 'str'
            elif isinstance(value, list):
                type_annotation = 'list'
            elif isinstance(value, dict):
                type_annotation = 'dict'
            elif value is None:
                type_annotation = 'None'
            else:
                type_annotation = 'unknown'
        
        # Type enforcement if type annotation is provided (but not for class objects)
        if (type_annotation and type_annotation != 'unknown' and 
            not self._check_type(value, type_annotation)):
            # Create enhanced error message with context
            error_msg = (f"Type mismatch for parameter '{name}': expected {type_annotation}, "
                        f"got {self._get_type_name(value)}")
            if self.interpreter:
                raise self.interpreter._create_runtime_error(error_msg)
            else:
                raise RuntimeErrorLyric(error_msg)
        
        self.variables[name] = value
        self.variable_types[name] = type_annotation
        self._cache[name] = value  # Update cache
        self._invalidate_parent_cache()  # Invalidate parent caches
    
    def _invalidate_parent_cache(self):
        """Invalidate cache for all parent environments."""
        if self.parent:
            self.parent._cache_valid = False
            self.parent._invalidate_parent_cache()
    
    
    def _get_type_name(self, value: Any) -> str:
        """Get the type name of a value."""
        if isinstance(value, bool):
            return 'bool'
        elif isinstance(value, int):
            return 'int'
        elif isinstance(value, float):
            return 'float'
        elif isinstance(value, str):
            return 'str'
        elif isinstance(value, list):
            return 'list'
        elif isinstance(value, dict):
            return 'dict'
        elif value is None:
            return 'None'
        else:
            return type(value).__name__

    def _check_type(self, value: Any, expected_type: str) -> bool:
        """Check if a value matches the expected type."""
        if expected_type == 'bool' and isinstance(value, bool):
            return True
        elif expected_type == 'int' and isinstance(value, int) and not isinstance(value, bool):
            return True
        elif expected_type == 'float' and isinstance(value, float):
            return True
        elif expected_type == 'str' and isinstance(value, str):
            return True
        elif expected_type == 'list' and isinstance(value, list):
            return True
        elif expected_type == 'dict' and isinstance(value, dict):
            return True
        elif expected_type == 'None' and value is None:
            return True
        else:
            # Check for custom class types
            from lyric.interpreter import Instance
            if isinstance(value, Instance) and expected_type == value.class_obj.name:
                return True
        return False

    def _get_type_name(self, value: Any) -> str:
        """Get the type name of a value."""
        if isinstance(value, bool):
            return 'bool'
        elif isinstance(value, int):
            return 'int'
        elif isinstance(value, float):
            return 'float'
        elif isinstance(value, str):
            return 'str'
        elif isinstance(value, list):
            return 'list'
        elif isinstance(value, dict):
            return 'dict'
        elif value is None:
            return 'None'
        else:
            from lyric.interpreter import Instance
            if isinstance(value, Instance):
                return value.class_obj.name
            return 'unknown'

    def get_type(self, name: str) -> Optional[str]:
        """Get the type of a variable."""
        if name in self.variable_types:
            return self.variable_types[name]
        
        if self.parent:
            return self.parent.get_type(name)
        
        return None

    def get(self, name: str) -> Any:
        """Get a variable value, looking up the chain of environments with caching."""
        # Record variable lookup for performance monitoring
        if self.interpreter:
            self.interpreter._record_variable_lookup()
        
        # Check local variables first
        if name in self.variables:
            return self.variables[name]
        
        # Check cache if valid
        if self._cache_valid and name in self._cache:
            return self._cache[name]

        # Look up in parent environments
        if self.parent:
            value = self.parent.get(name)
            # Cache the result for future lookups
            if self._cache_valid:
                self._cache[name] = value
            return value

        # Use enhanced error if interpreter is available
        if self.interpreter:
            raise self.interpreter._create_runtime_error(f"Undefined variable: {name}")
        else:
            raise RuntimeErrorLyric(f"Undefined variable: {name}")

    def assign(self, name: str, value: Any) -> None:
        """Assign a value to a variable, looking up the chain if needed."""
        if name in self.variables:
            # Check if this variable has a type annotation and enforce it
            existing_type = self.variable_types.get(name)
            if existing_type and existing_type != 'unknown':
                if not self._check_type(value, existing_type):
                    error_msg = (f"Type mismatch for variable '{name}': expected {existing_type}, "
                               f"got {self._get_type_name(value)}")
                    if self.interpreter:
                        raise self.interpreter._create_runtime_error(error_msg)
                    else:
                        raise RuntimeErrorLyric(error_msg)
            
            self.variables[name] = value
            self._cache[name] = value  # Update cache
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise RuntimeErrorLyric(f"Undefined variable: {name}")


class Function:
    """Represents a user-defined function."""

    def __init__(self, node: FunctionNode, closure: Environment):
        self.node = node
        self.closure = closure

    def call(self, interpreter: 'Interpreter', arguments: List[Any]) -> Any:
        """Call this function with the given arguments."""
        # Record function call for performance monitoring
        interpreter._record_function_call(self.node.name)
        
        # Create new environment for function execution
        env = Environment(self.closure, interpreter)

        try:
            # Add environment to call stack
            interpreter.call_stack.append(env)

            # Bind parameters to arguments with type checking
            for i, (param, arg) in enumerate(zip(self.node.params, arguments)):
                # Get type annotation for this parameter if available
                param_type = None
                if self.node.param_types and i < len(self.node.param_types):
                    param_type = self.node.param_types[i]
                
                try:
                    env.define(param, arg, param_type)
                except RuntimeErrorLyric as e:
                    # Enhance error with function call context
                    enhanced_msg = (f"In function '{self.node.name}': {str(e)}. "
                                  f"Called with argument {i+1} ({param}) = {repr(arg)}")
                    if interpreter:
                        raise interpreter._create_runtime_error(enhanced_msg)
                    else:
                        raise RuntimeErrorLyric(enhanced_msg)

            # Push stack frame for this function call (after parameters are bound)
            interpreter._push_stack_frame(
                self.node.name, 
                getattr(self.node, 'filename', 'unknown'), 
                getattr(self.node, 'line', 0),
                getattr(self.node, 'col', 0),
                env=env
            )

            # Execute function body
            result = interpreter._execute_block(self.node.body_statements, env)
            
            # Check return type if specified
            if self.node.return_type:
                expected_type = self.node.return_type
                if not env._check_type(result, expected_type):
                    error_msg = (f"Function '{self.node.name}' return type mismatch: "
                               f"expected {expected_type}, got {env._get_type_name(result)} "
                               f"(returned value: {repr(result)})")
                    raise interpreter._create_runtime_error(error_msg)
            
            return result
        
        finally:
            # Pop stack frame and environment
            interpreter._pop_stack_frame()
            interpreter.call_stack.pop()


class Class:
    """Represents a user-defined class.

    A Class object contains the class definition including methods and attributes.
    It can be called as a constructor to create new instances.
    """

    def __init__(self, name: str, methods: Dict[str, Function], attributes: Dict[str, Any]):
        """Initialize a Class object.

        Args:
            name: The name of the class
            methods: Dictionary mapping method names to Function objects
            attributes: Dictionary mapping attribute names to their values
        """
        self.name = name
        self.methods = methods
        self.attributes = attributes

    def instantiate(self) -> 'Instance':
        """Create a new instance of this class.

        Returns:
            A new Instance object with copied class attributes
        """
        # Copy class attributes to instance
        instance_attributes = self.attributes.copy()
        return Instance(self, instance_attributes)

    def call(self, interpreter: 'Interpreter', arguments: List[Any]) -> 'Instance':
        """Call the class as a constructor (e.g., Player()).

        Args:
            interpreter: The interpreter instance
            arguments: Constructor arguments (currently not supported)

        Returns:
            A new Instance object

        Raises:
            RuntimeErrorLyric: If arguments are provided (not yet supported)
        """
        if arguments:
            raise RuntimeErrorLyric(f"Class constructor '{self.name}' does not accept arguments")
        return self.instantiate()


class Instance:
    """Represents an instance of a class.

    An Instance object contains instance-specific attributes and provides access
    to class methods bound to the instance.
    """

    def __init__(self, class_obj: Class, attributes: Dict[str, Any]):
        """Initialize an Instance object.

        Args:
            class_obj: The Class object this instance belongs to
            attributes: Dictionary of instance attributes
        """
        self.class_obj = class_obj
        self.attributes = attributes

    def get_attribute(self, name: str) -> Any:
        """Get an attribute from this instance.

        Args:
            name: The name of the attribute to get

        Returns:
            The attribute value or a bound method

        Raises:
            RuntimeErrorLyric: If the attribute doesn't exist
        """
        if name in self.attributes:
            return self.attributes[name]
        elif name in self.class_obj.methods:
            # Return a bound method
            method = self.class_obj.methods[name]
            return BoundMethod(method, self)
        else:
            raise RuntimeErrorLyric(f"Instance of '{self.class_obj.name}' has no attribute "
                                    f"'{name}'")

    def set_attribute(self, name: str, value: Any) -> None:
        """Set an attribute on this instance.

        Args:
            name: The name of the attribute to set
            value: The value to assign to the attribute
        """
        self.attributes[name] = value


class BoundMethod:
    """Represents a method bound to an instance.

    A BoundMethod object represents a method that has been bound to a specific
    instance, allowing it to access the instance's attributes via 'self'.
    """

    def __init__(self, method: Function, instance: Instance):
        """Initialize a BoundMethod object.

        Args:
            method: The Function object representing the method
            instance: The Instance object this method is bound to
        """
        self.method = method
        self.instance = instance

    def call(self, interpreter: 'Interpreter', arguments: List[Any]) -> Any:
        """Call this bound method.

        Args:
            interpreter: The interpreter instance
            arguments: Method arguments

        Returns:
            The result of executing the method
        """
        # Create new environment for method execution
        env = Environment(self.method.closure)

        # Bind 'self' to the instance
        env.define('self', self.instance)

        # Bind parameters to arguments
        for param, arg in zip(self.method.node.params, arguments):
            env.define(param, arg)

        # Execute method body
        return interpreter._execute_block(self.method.node.body_statements, env)


class Interpreter:
    """Interpreter for executing Lyric AST nodes."""

    def __init__(self, debug_mode: bool = False, performance_monitoring: bool = False):
        self.global_env = Environment(interpreter=self)
        self.functions: Dict[str, Function] = {}
        self.call_stack: List[Environment] = []
        self.stack_frames: List[StackFrame] = []  # For stack trace tracking
        self.debug_mode = debug_mode
        self.performance_monitoring = performance_monitoring
        
        # Performance monitoring data
        self._operation_counts: Dict[str, int] = {}
        self._function_call_counts: Dict[str, int] = {}
        self._variable_lookup_counts: int = 0
        self._constant_fold_count: int = 0

        # Initialize built-in functions
        self._init_builtins()
    
    def _record_operation(self, operation: str):
        """Record an operation for performance monitoring."""
        if self.performance_monitoring:
            self._operation_counts[operation] = self._operation_counts.get(operation, 0) + 1
    
    def _record_function_call(self, function_name: str):
        """Record a function call for performance monitoring."""
        if self.performance_monitoring:
            self._function_call_counts[function_name] = self._function_call_counts.get(function_name, 0) + 1
    
    def _record_variable_lookup(self):
        """Record a variable lookup for performance monitoring."""
        if self.performance_monitoring:
            self._variable_lookup_counts += 1
    
    def _record_constant_fold(self):
        """Record a constant folding optimization for performance monitoring."""
        if self.performance_monitoring:
            self._constant_fold_count += 1
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance monitoring statistics."""
        if not self.performance_monitoring:
            return {"performance_monitoring": False}
        
        return {
            "performance_monitoring": True,
            "operation_counts": self._operation_counts.copy(),
            "function_call_counts": self._function_call_counts.copy(),
            "variable_lookup_count": self._variable_lookup_counts,
            "constant_fold_count": self._constant_fold_count,
            "total_operations": sum(self._operation_counts.values()),
            "total_function_calls": sum(self._function_call_counts.values())
        }
    
    def reset_performance_stats(self):
        """Reset performance monitoring statistics."""
        self._operation_counts.clear()
        self._function_call_counts.clear()
        self._variable_lookup_counts = 0
        self._constant_fold_count = 0

    def _init_builtins(self):
        """Initialize built-in functions."""
        # Register built-in functions in the global environment
        register_builtins(self.global_env.variables)
    
    def _push_stack_frame(self, function_name: str, filename: str, line: int, col: int = None, env: Environment = None):
        """Push a new frame onto the call stack."""
        local_vars = {}
        if env:
            # Get local variables from the function's environment
            local_vars = env.variables.copy()
        
        frame = StackFrame(function_name, filename, line, col, local_vars)
        self.stack_frames.append(frame)
    
    def _pop_stack_frame(self):
        """Pop the top frame from the call stack."""
        if self.stack_frames:
            self.stack_frames.pop()
    
    def _create_runtime_error(self, message: str, line: int = None, col: int = None, filename: str = None):
        """Create a RuntimeErrorLyric with stack trace information."""
        # Capture current stack state before any cleanup
        current_stack_frames = self.stack_frames.copy()
        current_call_stack = self.call_stack.copy()
        
        # Update stack frames with current variable states
        updated_frames = []
        for i, frame in enumerate(current_stack_frames):
            # Get current environment for this frame level
            if i < len(current_call_stack):
                current_env = current_call_stack[i]
                updated_local_vars = current_env.variables.copy()
            else:
                updated_local_vars = frame.local_vars.copy()
            
            updated_frame = StackFrame(
                frame.function_name, 
                frame.filename, 
                frame.line, 
                frame.col, 
                updated_local_vars
            )
            updated_frames.append(updated_frame)
        
        # Use filename and line from current stack frame if not provided
        if filename is None and updated_frames:
            filename = updated_frames[-1].filename
        if line is None and updated_frames:
            line = updated_frames[-1].line
        
        return RuntimeErrorLyric(
            message, 
            line=line, 
            col=col, 
            filename=filename, 
            stack_trace=updated_frames
        )

    def interpret(self, program: ProgramNode) -> None:
        """Interpret a complete program."""
        # Execute all statements in the global environment
        for statement in program.statements:
            self._execute_statement(statement, self.global_env)

        # Automatically call main() if it exists
        if 'main' in self.functions:
            main_func = self.functions['main']
            main_func.call(self, [])

    def _execute_statement(self, stmt: Any, env: Environment) -> Any:
        """Execute a single statement."""
        if isinstance(stmt, FunctionNode):
            return self._execute_function_def(stmt, env)
        elif isinstance(stmt, ClassNode):
            return self._execute_class_def(stmt, env)
        elif isinstance(stmt, AssignNode):
            return self._execute_assignment(stmt, env)
        elif isinstance(stmt, CallNode):
            return self._execute_call(stmt, env)
        elif isinstance(stmt, MethodCallNode):
            return self._execute_method_call(stmt, env)
        elif isinstance(stmt, PrintNode):
            return self._execute_print(stmt, env)
        elif isinstance(stmt, IfNode):
            return self._execute_if(stmt, env)
        elif isinstance(stmt, LoopNode):
            return self._execute_loop(stmt, env)
        elif isinstance(stmt, ReturnNode):
            return self._execute_return(stmt, env)
        elif isinstance(stmt, ImportNode):
            return self._execute_import(stmt, env)
        else:
            # Try to evaluate as expression
            return self._evaluate_expression(stmt, env)
    
    def _execute_block(self, statements: List[Any], env: Environment) -> Any:
        """Execute a block of statements."""
        result = None
        for stmt in statements:
            result = self._execute_statement(stmt, env)
        return result

    def _execute_function_def(self, stmt: FunctionNode, env: Environment) -> None:
        """Execute a function definition."""
        func = Function(stmt, env)
        self.functions[stmt.name] = func

    def _execute_class_def(self, stmt: ClassNode, env: Environment) -> None:
        """Execute a class definition.

        Args:
            stmt: The ClassNode to execute
            env: The environment to define the class in
        """
        # Create class environment for evaluating class members
        class_env = Environment(env)

        # Separate class attributes and methods
        class_attributes = {}
        class_methods = {}

        for member in stmt.members_statements:
            if isinstance(member, AssignNode):
                # Class attribute
                value = self._evaluate_expression(member.expr, class_env)
                # Extract the name from the assignment target
                if isinstance(member.name, str):
                    name = member.name
                elif isinstance(member.name, IdentifierNode):
                    name = member.name.name
                else:
                    raise RuntimeErrorLyric(f"Invalid class attribute name: {type(member.name)}")
                class_attributes[name] = value
            elif isinstance(member, FunctionNode):
                # Class method
                func = Function(member, class_env)
                class_methods[member.name] = func

        # Create the class object
        class_obj = Class(stmt.name, class_methods, class_attributes)

        # Register the class in the environment
        env.define(stmt.name, class_obj)

    def _execute_assignment(self, stmt: AssignNode, env: Environment) -> Any:
        """Execute a variable assignment.

        Args:
            stmt: The AssignNode to execute
            env: The environment to execute in

        Returns:
            The assigned value

        Raises:
            RuntimeErrorLyric: If assignment target is invalid
        """
        value = self._evaluate_expression(stmt.expr, env)

        # Handle member access assignment (e.g., self.name = value)
        if isinstance(stmt.name, MemberAccessNode):
            obj = self._evaluate_expression(stmt.name.object, env)
            if isinstance(obj, Instance):
                obj.set_attribute(stmt.name.member, value)
                return value
            else:
                raise RuntimeErrorLyric(f"Cannot assign to member '{stmt.name.member}' on "
                                        f"non-instance object")
        elif isinstance(stmt.name, str):
            # Regular variable assignment with optional type annotation
            if stmt.type_annotation:
                # New variable with type annotation
                env.define(stmt.name, value, stmt.type_annotation)
            else:
                # Check if variable exists
                if stmt.name in env.variables:
                    # Reassign existing variable (with type checking)
                    env.assign(stmt.name, value)
                elif env.parent:
                    # Try to find in parent scope
                    try:
                        env.parent.assign(stmt.name, value)
                    except:
                        # Variable doesn't exist anywhere, define it
                        env.define(stmt.name, value)
                else:
                    # New variable without type annotation
                    env.define(stmt.name, value)
            return value
        elif isinstance(stmt.name, IdentifierNode):
            # Regular variable assignment from identifier with optional type annotation
            if stmt.type_annotation:
                # New variable with type annotation
                env.define(stmt.name.name, value, stmt.type_annotation)
            else:
                # Check if variable exists
                if stmt.name.name in env.variables:
                    # Reassign existing variable (with type checking)
                    env.assign(stmt.name.name, value)
                elif env.parent:
                    # Try to find in parent scope
                    try:
                        env.parent.assign(stmt.name.name, value)
                    except:
                        # Variable doesn't exist anywhere, define it
                        env.define(stmt.name.name, value)
                else:
                    # New variable without type annotation
                    env.define(stmt.name.name, value)
            return value
        else:
            raise RuntimeErrorLyric(f"Invalid assignment target: {type(stmt.name)}")

    def _execute_call(self, stmt: CallNode, env: Environment) -> Any:
        """Execute a function call."""
        # Evaluate arguments
        arguments = []
        for arg in stmt.args:
            arguments.append(self._evaluate_expression(arg, env))

        # Check if it's a built-in function
        if stmt.func_name in self.global_env.variables:
            builtin = self.global_env.variables[stmt.func_name]
            if isinstance(builtin, BuiltinFunction):
                return builtin.call(arguments)

        # Check if it's a class (for instantiation) - check local and global environments
        obj = None
        if stmt.func_name in env.variables:
            obj = env.variables[stmt.func_name]
        elif stmt.func_name in self.global_env.variables:
            obj = self.global_env.variables[stmt.func_name]

        if obj is not None and isinstance(obj, Class):
            return obj.call(self, arguments)

        # Check if it's a bound method
        if stmt.func_name in env.variables:
            obj = env.variables[stmt.func_name]
            if isinstance(obj, BoundMethod):
                return obj.call(self, arguments)

        # Check user-defined functions
        if stmt.func_name in self.functions:
            func = self.functions[stmt.func_name]
            return func.call(self, arguments)

        raise self._create_runtime_error(f"Undefined function: {stmt.func_name}")

    def _execute_print(self, stmt: PrintNode, env: Environment) -> None:
        """Execute a print statement."""
        arguments = []
        for arg in stmt.args:
            arguments.append(self._evaluate_expression(arg, env))

        # Use the built-in print function
        print_builtin = self.global_env.variables['print']
        print_builtin.call(arguments)

    def _execute_if(self, stmt: IfNode, env: Environment) -> Any:
        """Execute an if statement."""
        # Evaluate condition
        condition = self._evaluate_expression(stmt.condition, env)

        if self._is_truthy(condition):
            # Execute then body
            return self._execute_block(stmt.then_body, env)
        else:
            # Check elif clauses
            for elif_stmt in stmt.elifs:
                elif_condition = self._evaluate_expression(elif_stmt.condition, env)
                if self._is_truthy(elif_condition):
                    return self._execute_block(elif_stmt.body, env)

            # Execute else body if present
            if stmt.else_body:
                return self._execute_block(stmt.else_body, env)

        return None

    def _execute_loop(self, stmt: LoopNode, env: Environment) -> None:
        """Execute a loop statement."""
        if stmt.loop_kind == "iterator":
            # Iterator loop: "i in range(N)"
            if (isinstance(stmt.condition_or_iter, BinaryOpNode) and
                    stmt.condition_or_iter.op == "in"):
                var_name = stmt.condition_or_iter.left.name
                iterable = self._evaluate_expression(stmt.condition_or_iter.right, env)

                # Iterate over the iterable
                for item in iterable:
                    env.define(var_name, item)
                    self._execute_block(stmt.body, env)
            else:
                raise RuntimeErrorLyric("Iterator loop must be in the form 'variable in iterable'")
        else:
            # While loop: boolean condition
            while True:
                condition = self._evaluate_expression(stmt.condition_or_iter, env)
                if not self._is_truthy(condition):
                    break

                self._execute_block(stmt.body, env)

    def _execute_return(self, stmt: ReturnNode, env: Environment) -> Any:
        """Execute a return statement."""
        if stmt.expr:
            return self._evaluate_expression(stmt.expr, env)
        return None

    def _execute_import(self, stmt: ImportNode, env: Environment) -> None:
        """Execute an import statement."""
        # For now, imports are not implemented
        # In a full implementation, this would load modules
        pass

    def _execute_block(self, statements: List[Any], env: Environment) -> Any:
        """Execute a block of statements."""
        result = None
        for statement in statements:
            result = self._execute_statement(statement, env)
        return result

    def _evaluate_expression(self, expr: Any, env: Environment) -> Any:
        """Evaluate an expression."""
        if isinstance(expr, LiteralNode):
            # Handle list and dictionary literals that contain AST nodes
            if isinstance(expr.value, list):
                # Evaluate list elements
                return [self._evaluate_expression(element, env) for element in expr.value]
            elif isinstance(expr.value, dict):
                # Evaluate dictionary values (keys are already evaluated at parse time)
                evaluated_dict = {}
                for key, value_node in expr.value.items():
                    evaluated_dict[key] = self._evaluate_expression(value_node, env)
                return evaluated_dict
            else:
                # Regular literal value
                return expr.value
        elif isinstance(expr, IdentifierNode):
            return env.get(expr.name)
        elif isinstance(expr, MemberAccessNode):
            return self._evaluate_member_access(expr, env)
        elif isinstance(expr, IndexNode):
            return self._evaluate_indexing(expr, env)
        elif isinstance(expr, BinaryOpNode):
            return self._evaluate_binary_op(expr, env)
        elif isinstance(expr, UnaryOpNode):
            return self._evaluate_unary_op(expr, env)
        elif isinstance(expr, CallNode):
            return self._execute_call(expr, env)
        elif isinstance(expr, MethodCallNode):
            return self._execute_method_call(expr, env)
        else:
            raise RuntimeErrorLyric(f"Unknown expression type: {type(expr)}")

    def _execute_method_call(self, stmt: MethodCallNode, env: Environment) -> Any:
        """Execute a method call (object.method()).

        Args:
            stmt: The MethodCallNode to execute
            env: The environment to execute in

        Returns:
            The result of the method call

        Raises:
            RuntimeErrorLyric: If the object doesn't have the method
        """
        # Evaluate the object
        obj = self._evaluate_expression(stmt.object, env)

        # Evaluate arguments
        arguments = []
        for arg in stmt.args:
            arguments.append(self._evaluate_expression(arg, env))

        # Get the method from the object
        if isinstance(obj, Instance):
            method = obj.get_attribute(stmt.method)
            if isinstance(method, BoundMethod):
                return method.call(self, arguments)
            else:
                raise RuntimeErrorLyric(f"'{stmt.method}' is not a method")
        else:
            raise RuntimeErrorLyric(f"Cannot call method '{stmt.method}' on non-instance object")

    def _evaluate_member_access(self, expr: MemberAccessNode, env: Environment) -> Any:
        """Evaluate member access (object.attribute).

        Args:
            expr: The MemberAccessNode to evaluate
            env: The environment to evaluate in

        Returns:
            The value of the member

        Raises:
            RuntimeErrorLyric: If the object doesn't support member access
        """
        obj = self._evaluate_expression(expr.object, env)

        if isinstance(obj, Instance):
            return obj.get_attribute(expr.member)
        else:
            raise RuntimeErrorLyric(f"Cannot access member '{expr.member}' on non-instance object")

    def _evaluate_indexing(self, expr: IndexNode, env: Environment) -> Any:
        """Evaluate indexing operation (object[index]).
        
        Args:
            expr: The IndexNode to evaluate
            env: The environment to evaluate in
            
        Returns:
            The value at the specified index
            
        Raises:
            RuntimeErrorLyric: If indexing is invalid or index is out of bounds
        """
        obj = self._evaluate_expression(expr.object, env)
        index = self._evaluate_expression(expr.index, env)
        
        # Handle list indexing
        if isinstance(obj, list):
            if not isinstance(index, int):
                raise RuntimeErrorLyric(f"List indexing error: index must be an integer, got {type(index).__name__} (value: {repr(index)})")
            if index < 0 or index >= len(obj):
                raise RuntimeErrorLyric(f"List index {index} out of range (list has {len(obj)} elements, valid indices: 0 to {len(obj)-1})")
            return obj[index]
        
        # Handle dictionary indexing
        elif isinstance(obj, dict):
            if index not in obj:
                raise RuntimeErrorLyric(f"Dictionary key '{index}' not found (available keys: {list(obj.keys())})")
            return obj[index]
        
        # Handle string indexing (for convenience)
        elif isinstance(obj, str):
            if not isinstance(index, int):
                raise RuntimeErrorLyric(f"String indexing error: index must be an integer, got {type(index).__name__} (value: {repr(index)})")
            if index < 0 or index >= len(obj):
                raise RuntimeErrorLyric(f"String index {index} out of range (string has {len(obj)} characters, valid indices: 0 to {len(obj)-1})")
            return obj[index]
        
        else:
            raise RuntimeErrorLyric(f"Cannot index object of type {type(obj).__name__} (only lists, dictionaries, and strings support indexing)")

    def _evaluate_binary_op(self, expr: BinaryOpNode, env: Environment) -> Any:
        """Evaluate a binary operation with constant folding optimization."""
        # Record operation for performance monitoring
        self._record_operation(f"binary_{expr.op}")
        
        # Constant folding: if both operands are literals, evaluate at compile time
        if (isinstance(expr.left, LiteralNode) and isinstance(expr.right, LiteralNode) and
            not isinstance(expr.left.value, (list, dict)) and not isinstance(expr.right.value, (list, dict))):
            self._record_constant_fold()
            return self._fold_constant_binary_op(expr.op, expr.left.value, expr.right.value)
        
        # Evaluate operands normally
        left = self._evaluate_expression(expr.left, env)
        right = self._evaluate_expression(expr.right, env)

        if expr.op == '+':
            return left + right
        elif expr.op == '-':
            return left - right
        elif expr.op == '*':
            return left * right
        elif expr.op == '/':
            if right == 0:
                raise RuntimeErrorLyric("Arithmetic error: division by zero")
            return left / right
        elif expr.op == '%':
            if right == 0:
                raise RuntimeErrorLyric("Arithmetic error: modulo by zero")
            return left % right
        elif expr.op == '==':
            return left == right
        elif expr.op == '!=':
            return left != right
        elif expr.op == '<':
            return left < right
        elif expr.op == '<=':
            return left <= right
        elif expr.op == '>':
            return left > right
        elif expr.op == '>=':
            return left >= right
        elif expr.op == 'and':
            return self._is_truthy(left) and self._is_truthy(right)
        elif expr.op == 'or':
            return self._is_truthy(left) or self._is_truthy(right)
        elif expr.op == 'in':
            return right.__contains__(left)
        else:
            raise RuntimeErrorLyric(f"Unknown binary operator: {expr.op}")
    
    def _fold_constant_binary_op(self, op: str, left: Any, right: Any) -> Any:
        """Fold constant binary operations at compile time for performance optimization."""
        try:
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                if right == 0:
                    raise RuntimeErrorLyric("Arithmetic error: division by zero")
                return left / right
            elif op == '%':
                if right == 0:
                    raise RuntimeErrorLyric("Arithmetic error: modulo by zero")
                return left % right
            elif op == '==':
                return left == right
            elif op == '!=':
                return left != right
            elif op == '<':
                return left < right
            elif op == '<=':
                return left <= right
            elif op == '>':
                return left > right
            elif op == '>=':
                return left >= right
            elif op == 'and':
                return self._is_truthy(left) and self._is_truthy(right)
            elif op == 'or':
                return self._is_truthy(left) or self._is_truthy(right)
            elif op == 'in':
                return right.__contains__(left)
            else:
                raise RuntimeErrorLyric(f"Unknown binary operator: {op}")
        except (TypeError, ValueError) as e:
            # If constant folding fails, fall back to runtime evaluation
            raise RuntimeErrorLyric(f"Invalid operation {left} {op} {right}: {e}")

    def _evaluate_unary_op(self, expr: UnaryOpNode, env: Environment) -> Any:
        """Evaluate a unary operation with constant folding optimization."""
        # Record operation for performance monitoring
        self._record_operation(f"unary_{expr.op}")
        
        # Constant folding: if operand is a literal, evaluate at compile time
        if isinstance(expr.operand, LiteralNode) and not isinstance(expr.operand.value, (list, dict)):
            self._record_constant_fold()
            return self._fold_constant_unary_op(expr.op, expr.operand.value)
        
        # Evaluate operand normally
        operand = self._evaluate_expression(expr.operand, env)

        if expr.op == '-':
            return -operand
        elif expr.op == '+':
            return +operand
        elif expr.op == '!' or expr.op == 'not':
            return not self._is_truthy(operand)
        else:
            raise RuntimeErrorLyric(f"Unknown unary operator: {expr.op}")
    
    def _fold_constant_unary_op(self, op: str, operand: Any) -> Any:
        """Fold constant unary operations at compile time for performance optimization."""
        try:
            if op == '-':
                return -operand
            elif op == '+':
                return +operand
            elif op == '!' or op == 'not':
                return not self._is_truthy(operand)
            else:
                raise RuntimeErrorLyric(f"Unknown unary operator: {op}")
        except (TypeError, ValueError) as e:
            # If constant folding fails, fall back to runtime evaluation
            raise RuntimeErrorLyric(f"Invalid operation {op}{operand}: {e}")

    def _is_truthy(self, value: Any) -> bool:
        """Determine if a value is truthy."""
        if value is None:
            return False
        elif isinstance(value, bool):
            return value
        elif isinstance(value, (int, float)):
            return value != 0
        elif isinstance(value, str):
            return len(value) > 0
        elif isinstance(value, list):
            return len(value) > 0
        else:
            return True


def interpret(program: ProgramNode) -> None:
    """Interpret a program node.

    Args:
        program: The parsed program to execute
    """
    interpreter = Interpreter()
    interpreter.interpret(program)
