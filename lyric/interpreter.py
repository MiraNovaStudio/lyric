"""
Interpreter module for the Lyric language.
Executes AST nodes to run programs.
"""

from typing import Dict, List, Any, Optional
from lyric.ast import (
    ProgramNode, FunctionNode, ClassNode, IfNode, ElifNode, LoopNode,
    AssignNode, CallNode, BinaryOpNode, UnaryOpNode, LiteralNode,
    IdentifierNode, PrintNode, ImportNode, ReturnNode
)
from lyric.errors import RuntimeErrorLyric
from lyric.runtime import register_builtins, BuiltinFunction


class Environment:
    """Represents a local environment (scope) for variable storage."""
    
    def __init__(self, parent: Optional['Environment'] = None):
        self.variables: Dict[str, Any] = {}
        self.parent = parent
    
    def define(self, name: str, value: Any) -> None:
        """Define a variable in this environment."""
        self.variables[name] = value
    
    def get(self, name: str) -> Any:
        """Get a variable value, looking up the chain of environments."""
        if name in self.variables:
            return self.variables[name]
        
        if self.parent:
            return self.parent.get(name)
        
        raise RuntimeErrorLyric(f"Undefined variable: {name}")
    
    def assign(self, name: str, value: Any) -> None:
        """Assign a value to a variable, looking up the chain if needed."""
        if name in self.variables:
            self.variables[name] = value
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
        # Create new environment for function execution
        env = Environment(self.closure)
        
        # Bind parameters to arguments
        for param, arg in zip(self.node.params, arguments):
            env.define(param, arg)
        
        # Execute function body
        return interpreter._execute_block(self.node.body_statements, env)


class Interpreter:
    """Interpreter for executing Lyric AST nodes."""
    
    def __init__(self):
        self.global_env = Environment()
        self.functions: Dict[str, Function] = {}
        self.call_stack: List[Environment] = []
        
        # Initialize built-in functions
        self._init_builtins()
    
    def _init_builtins(self):
        """Initialize built-in functions."""
        # Register built-in functions in the global environment
        register_builtins(self.global_env.variables)
    
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
    
    def _execute_function_def(self, stmt: FunctionNode, env: Environment) -> None:
        """Execute a function definition."""
        func = Function(stmt, env)
        self.functions[stmt.name] = func
    
    def _execute_class_def(self, stmt: ClassNode, env: Environment) -> None:
        """Execute a class definition."""
        # For now, classes are just containers for variables and methods
        # We'll store the class definition in the environment
        class_obj = {}
        
        # Execute class members
        class_env = Environment(env)
        for member in stmt.members_statements:
            if isinstance(member, AssignNode):
                # Class variable
                value = self._evaluate_expression(member.expr, class_env)
                class_obj[member.name] = value
            elif isinstance(member, FunctionNode):
                # Class method
                func = Function(member, class_env)
                self.functions[member.name] = func
        
        env.define(stmt.name, class_obj)
    
    def _execute_assignment(self, stmt: AssignNode, env: Environment) -> Any:
        """Execute a variable assignment."""
        value = self._evaluate_expression(stmt.expr, env)
        env.define(stmt.name, value)
        return value
    
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
        
        # Check user-defined functions
        if stmt.func_name in self.functions:
            func = self.functions[stmt.func_name]
            return func.call(self, arguments)
        
        raise RuntimeErrorLyric(f"Undefined function: {stmt.func_name}")
    
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
            if isinstance(stmt.condition_or_iter, BinaryOpNode) and stmt.condition_or_iter.op == "in":
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
            return expr.value
        elif isinstance(expr, IdentifierNode):
            return env.get(expr.name)
        elif isinstance(expr, BinaryOpNode):
            return self._evaluate_binary_op(expr, env)
        elif isinstance(expr, UnaryOpNode):
            return self._evaluate_unary_op(expr, env)
        elif isinstance(expr, CallNode):
            return self._execute_call(expr, env)
        else:
            raise RuntimeErrorLyric(f"Unknown expression type: {type(expr)}")
    
    def _evaluate_binary_op(self, expr: BinaryOpNode, env: Environment) -> Any:
        """Evaluate a binary operation."""
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
                raise RuntimeErrorLyric("Division by zero")
            return left / right
        elif expr.op == '%':
            if right == 0:
                raise RuntimeErrorLyric("Modulo by zero")
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
    
    def _evaluate_unary_op(self, expr: UnaryOpNode, env: Environment) -> Any:
        """Evaluate a unary operation."""
        operand = self._evaluate_expression(expr.operand, env)
        
        if expr.op == '-':
            return -operand
        elif expr.op == '+':
            return +operand
        elif expr.op == '!' or expr.op == 'not':
            return not self._is_truthy(operand)
        else:
            raise RuntimeErrorLyric(f"Unknown unary operator: {expr.op}")
    
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
