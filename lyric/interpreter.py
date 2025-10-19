"""
Lyric Language Interpreter
Executes parsed programs.
"""

from lyric.ast import *
from lyric.errors import RuntimeErrorLyric


class Interpreter:
    """Interpreter for the Lyric language."""
    
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.builtins = {
            'print': self._builtin_print,
            'range': self._builtin_range,
        }
    
    def interpret(self, ast):
        """Interpret an AST."""
        if isinstance(ast, ProgramNode):
            return self._interpret_program(ast)
        else:
            return self._interpret_node(ast)
    
    def _interpret_program(self, node):
        """Interpret a program node."""
        result = None
        for statement in node.statements:
            result = self._interpret_node(statement)
        return result
    
    def _interpret_node(self, node):
        """Interpret any AST node."""
        if isinstance(node, FunctionNode):
            return self._interpret_function(node)
        elif isinstance(node, IfNode):
            return self._interpret_if(node)
        elif isinstance(node, GivenNode):
            return self._interpret_given(node)
        elif isinstance(node, AssignmentNode):
            return self._interpret_assignment(node)
        elif isinstance(node, BinaryOpNode):
            return self._interpret_binary_op(node)
        elif isinstance(node, UnaryOpNode):
            return self._interpret_unary_op(node)
        elif isinstance(node, VariableNode):
            return self._interpret_variable(node)
        elif isinstance(node, LiteralNode):
            return self._interpret_literal(node)
        elif isinstance(node, FunctionCallNode):
            return self._interpret_function_call(node)
        elif isinstance(node, BlockNode):
            return self._interpret_block(node)
        else:
            return None
    
    def _interpret_function(self, node):
        """Interpret a function definition."""
        self.functions[node.name] = node
        return None
    
    def _interpret_if(self, node):
        """Interpret an if statement."""
        condition = self._interpret_node(node.condition)
        
        if self._is_truthy(condition):
            return self._interpret_node(node.then_body)
        elif node.else_body:
            return self._interpret_node(node.else_body)
        
        return None
    
    def _interpret_given(self, node):
        """Interpret a given loop."""
        iterable = self._interpret_node(node.iterable)
        result = None
        
        if isinstance(iterable, list):
            for item in iterable:
                self.variables[node.variable] = item
                result = self._interpret_node(node.body)
        elif isinstance(iterable, range):
            for item in iterable:
                self.variables[node.variable] = item
                result = self._interpret_node(node.body)
        
        return result
    
    def _interpret_assignment(self, node):
        """Interpret an assignment."""
        value = self._interpret_node(node.value)
        self.variables[node.name] = value
        return value
    
    def _interpret_binary_op(self, node):
        """Interpret a binary operation."""
        left = self._interpret_node(node.left)
        right = self._interpret_node(node.right)
        
        if node.op == 'PLUS':
            return left + right
        elif node.op == 'MINUS':
            return left - right
        elif node.op == 'MULTIPLY':
            return left * right
        elif node.op == 'DIVIDE':
            return left / right
        elif node.op == 'EQUAL':
            return left == right
        elif node.op == 'NOTEQUAL':
            return left != right
        elif node.op == 'LESS':
            return left < right
        elif node.op == 'LESSEQUAL':
            return left <= right
        elif node.op == 'GREATER':
            return left > right
        elif node.op == 'GREATEREQUAL':
            return left >= right
        elif node.op == 'and':
            return self._is_truthy(left) and self._is_truthy(right)
        elif node.op == 'or':
            return self._is_truthy(left) or self._is_truthy(right)
        
        raise RuntimeErrorLyric(f"Unknown binary operator: {node.op}")
    
    def _interpret_unary_op(self, node):
        """Interpret a unary operation."""
        operand = self._interpret_node(node.operand)
        
        if node.op == 'not':
            return not self._is_truthy(operand)
        elif node.op == 'MINUS':
            return -operand
        
        raise RuntimeErrorLyric(f"Unknown unary operator: {node.op}")
    
    def _interpret_variable(self, node):
        """Interpret a variable reference."""
        if node.name in self.variables:
            return self.variables[node.name]
        elif node.name in self.builtins:
            return self.builtins[node.name]
        else:
            raise RuntimeErrorLyric(f"Undefined variable: {node.name}")
    
    def _interpret_literal(self, node):
        """Interpret a literal value."""
        return node.value
    
    def _interpret_function_call(self, node):
        """Interpret a function call."""
        if node.name in self.builtins:
            args = [self._interpret_node(arg) for arg in node.args]
            return self.builtins[node.name](*args)
        elif node.name in self.functions:
            func = self.functions[node.name]
            # Create new scope for function
            old_variables = self.variables.copy()
            self.variables = {}
            
            # Set parameters
            for i, param in enumerate(func.params):
                if i < len(node.args):
                    self.variables[param] = self._interpret_node(node.args[i])
            
            # Execute function body
            result = self._interpret_node(func.body)
            
            # Restore scope
            self.variables = old_variables
            
            return result
        else:
            raise RuntimeErrorLyric(f"Undefined function: {node.name}")
    
    def _interpret_block(self, node):
        """Interpret a block of statements."""
        result = None
        for statement in node.statements:
            result = self._interpret_node(statement)
        return result
    
    def _is_truthy(self, value):
        """Check if a value is truthy."""
        if value is None:
            return False
        elif isinstance(value, bool):
            return value
        elif isinstance(value, (int, float)):
            return value != 0
        elif isinstance(value, str):
            return len(value) > 0
        elif isinstance(value, (list, dict)):
            return len(value) > 0
        else:
            return True
    
    def _builtin_print(self, *args):
        """Built-in print function."""
        print(*args)
        return None
    
    def _builtin_range(self, *args):
        """Built-in range function."""
        if len(args) == 1:
            return list(range(args[0]))
        elif len(args) == 2:
            return list(range(args[0], args[1]))
        elif len(args) == 3:
            return list(range(args[0], args[1], args[2]))
        else:
            raise RuntimeErrorLyric("range() takes 1-3 arguments")
