"""Interpreter module for executing Lyric AST nodes."""

from typing import Any, Dict, List, Optional
from lyric.ast_nodes import (
    ProgramNode, FunctionNode, IfNode, LoopNode, AssignNode, CallNode,
    BinaryOpNode, UnaryOpNode, LiteralNode, IdentifierNode, ClassNode, PrintNode
)
from lyric.errors import RuntimeErrorLyric


class Interpreter:
    """Interpreter for executing Lyric AST nodes."""
    
    def __init__(self):
        self.global_scope = {
            'true': True,
            'false': False
        }
        self.functions = {}
        self.classes = {}
    
    def evaluate(self, ast: ProgramNode) -> Any:
        """Evaluate a ProgramNode and return the result."""
        try:
            # Evaluate all statements in the program
            for statement in ast.statements:
                self._evaluate_statement(statement)
            
            # If there's a main function, call it
            if "main" in self.functions:
                self._call_function("main", [])
            
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
            body = func_def['body']
            
            # Create local scope
            local_scope = {}
            for i, param in enumerate(params):
                if i < len(args):
                    local_scope[param] = args[i]
                else:
                    local_scope[param] = None
            
            # Save current scope
            old_scope = self.global_scope.copy()
            
            # Set local scope
            self.global_scope.update(local_scope)
            
            try:
                # Execute function body
                result = None
                for statement in body:
                    result = self._evaluate_statement(statement)
                return result
            finally:
                # Restore scope
                self.global_scope = old_scope
        else:
            raise RuntimeErrorLyric(f"Function '{func_name}' is not defined")
    
    def _evaluate_statement(self, statement) -> Any:
        """Evaluate a single statement."""
        if isinstance(statement, AssignNode):
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
        else:
            # Expression statement
            return self._evaluate_expression(statement)
    
    def _evaluate_assignment(self, node: AssignNode) -> Any:
        """Evaluate an assignment statement."""
        value = self._evaluate_expression(node.expr)
        self.global_scope[node.name] = value
        return value
    
    def _evaluate_function_definition(self, node: FunctionNode) -> None:
        """Evaluate a function definition."""
        self.functions[node.name] = {
            'params': node.params,
            'body': node.body_statements
        }
    
    def _evaluate_class_definition(self, node: ClassNode) -> None:
        """Evaluate a class definition."""
        class_dict = {}
        for member in node.members_statements:
            if isinstance(member, AssignNode):
                # Class member assignment
                value = self._evaluate_expression(member.expr)
                class_dict[member.name] = value
            elif isinstance(member, FunctionNode):
                # Class method
                class_dict[member.name] = {
                    'params': member.params,
                    'body': member.body_statements
                }
        
        self.classes[node.name] = class_dict
    
    def _evaluate_if_statement(self, node: IfNode) -> Any:
        """Evaluate an if statement."""
        condition = self._evaluate_expression(node.condition)
        
        if self._is_truthy(condition):
            # Execute then body
            for statement in node.then_body:
                self._evaluate_statement(statement)
        else:
            # Check elif clauses
            for elif_condition, elif_body in node.elifs:
                elif_result = self._evaluate_expression(elif_condition)
                if self._is_truthy(elif_result):
                    for statement in elif_body:
                        self._evaluate_statement(statement)
                    return None
            
            # Execute else body if it exists
            if node.else_body:
                for statement in node.else_body:
                    self._evaluate_statement(statement)
        
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
            # Evaluate range arguments
            args = [self._evaluate_expression(arg) for arg in node.condition_or_iter.args]
            
            if len(args) == 1:
                # range(n) -> 0 to n-1
                end = args[0]
                for i in range(end):
                    # Execute loop body
                    for statement in node.body:
                        self._evaluate_statement(statement)
            elif len(args) == 2:
                # range(start, end)
                start, end = args
                for i in range(start, end):
                    # Execute loop body
                    for statement in node.body:
                        self._evaluate_statement(statement)
            elif len(args) == 3:
                # range(start, end, step)
                start, end, step = args
                for i in range(start, end, step):
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
        if node.func_name == "print":
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
                raise RuntimeErrorLyric(f"range() takes 1-3 arguments, got {len(args)}")
        elif node.func_name in self.functions:
            # User-defined function
            args = [self._evaluate_expression(arg) for arg in node.args]
            return self._call_function(node.func_name, args)
        else:
            raise RuntimeErrorLyric(f"Function '{node.func_name}' is not defined")
    
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
        else:
            raise RuntimeErrorLyric(f"Unknown expression type: {type(expr)}")
    
    def _evaluate_identifier(self, node: IdentifierNode) -> Any:
        """Evaluate an identifier."""
        if '.' in node.name:
            # Member access: obj.member
            parts = node.name.split('.')
            obj_name = parts[0]
            member_name = parts[1]
            
            if obj_name in self.global_scope:
                obj = self.global_scope[obj_name]
                if isinstance(obj, dict) and member_name in obj:
                    return obj[member_name]
                else:
                    raise RuntimeErrorLyric(f"Member '{member_name}' not found in '{obj_name}'")
            else:
                raise RuntimeErrorLyric(f"Variable '{obj_name}' is not defined")
        else:
            # Simple identifier
            if node.name in self.global_scope:
                return self.global_scope[node.name]
            elif node.name in self.classes:
                # Class reference - return the class definition
                return self.classes[node.name]
            else:
                raise RuntimeErrorLyric(f"Variable '{node.name}' is not defined")
    
    def _evaluate_binary_operation(self, node: BinaryOpNode) -> Any:
        """Evaluate a binary operation."""
        left = self._evaluate_expression(node.left)
        right = self._evaluate_expression(node.right)
        
        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            if right == 0:
                raise RuntimeErrorLyric("Division by zero")
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
    
    def _evaluate_unary_operation(self, node: UnaryOpNode) -> Any:
        """Evaluate a unary operation."""
        operand = self._evaluate_expression(node.operand)
        
        if node.op == '-':
            return -operand
        elif node.op == '!' or node.op == 'not':
            return not self._is_truthy(operand)
        else:
            raise RuntimeErrorLyric(f"Unknown unary operator: {node.op}")
    
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