"""AST node definitions for Lyric language."""

from dataclasses import dataclass
from typing import List, Optional, Any, Union


@dataclass
class ProgramNode:
    """Represents the root of a Lyric program."""
    statements: List['ASTNode']
    
    def __repr__(self):
        return f"ProgramNode(statements={len(self.statements)})"
    
    def to_dict(self):
        return {
            'type': 'ProgramNode',
            'statements': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.statements]
        }


@dataclass
class FunctionNode:
    """Represents a function definition."""
    name: str
    params: List[str]
    body_statements: List['ASTNode']
    
    def __repr__(self):
        return f"FunctionNode(name='{self.name}', params={self.params}, body={len(self.body_statements)})"
    
    def to_dict(self):
        return {
            'type': 'FunctionNode',
            'name': self.name,
            'params': self.params,
            'body': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.body_statements]
        }


@dataclass
class IfNode:
    """Represents an if/elif/else statement."""
    condition: 'ASTNode'
    then_body: List['ASTNode']
    elifs: List[tuple['ASTNode', List['ASTNode']]]  # List of (condition, body) tuples
    else_body: Optional[List['ASTNode']]
    
    def __repr__(self):
        elif_count = len(self.elifs)
        else_present = self.else_body is not None
        return f"IfNode(condition={self.condition}, then={len(self.then_body)}, elifs={elif_count}, else={else_present})"
    
    def to_dict(self):
        return {
            'type': 'IfNode',
            'condition': self.condition.to_dict() if hasattr(self.condition, 'to_dict') else str(self.condition),
            'then_body': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.then_body],
            'elifs': [(cond.to_dict() if hasattr(cond, 'to_dict') else str(cond), 
                      [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in body]) 
                     for cond, body in self.elifs],
            'else_body': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.else_body] if self.else_body else None
        }


@dataclass
class LoopNode:
    """Represents a loop statement (given/done)."""
    condition_or_iter: 'ASTNode'
    loop_kind: str  # "iterator" or "while"
    body: List['ASTNode']
    iterator_var: Optional[str] = None  # Variable name for iterator loops
    
    def __repr__(self):
        return f"LoopNode(kind='{self.loop_kind}', condition={self.condition_or_iter}, body={len(self.body)}, iterator_var={self.iterator_var})"
    
    def to_dict(self):
        return {
            'type': 'LoopNode',
            'loop_kind': self.loop_kind,
            'condition_or_iter': self.condition_or_iter.to_dict() if hasattr(self.condition_or_iter, 'to_dict') else str(self.condition_or_iter),
            'body': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.body],
            'iterator_var': self.iterator_var
        }


@dataclass
class AssignNode:
    """Represents a variable assignment."""
    name: str
    expr: 'ASTNode'
    
    def __repr__(self):
        return f"AssignNode(name='{self.name}', expr={self.expr})"
    
    def to_dict(self):
        return {
            'type': 'AssignNode',
            'name': self.name,
            'expr': self.expr.to_dict() if hasattr(self.expr, 'to_dict') else str(self.expr)
        }


@dataclass
class CallNode:
    """Represents a function call."""
    func_name: str
    args: List['ASTNode']
    
    def __repr__(self):
        return f"CallNode(func='{self.func_name}', args={len(self.args)})"
    
    def to_dict(self):
        return {
            'type': 'CallNode',
            'func_name': self.func_name,
            'args': [arg.to_dict() if hasattr(arg, 'to_dict') else str(arg) for arg in self.args]
        }


@dataclass
class BinaryOpNode:
    """Represents a binary operation."""
    op: str
    left: 'ASTNode'
    right: 'ASTNode'
    
    def __repr__(self):
        return f"BinaryOpNode(op='{self.op}', left={self.left}, right={self.right})"
    
    def to_dict(self):
        return {
            'type': 'BinaryOpNode',
            'op': self.op,
            'left': self.left.to_dict() if hasattr(self.left, 'to_dict') else str(self.left),
            'right': self.right.to_dict() if hasattr(self.right, 'to_dict') else str(self.right)
        }


@dataclass
class UnaryOpNode:
    """Represents a unary operation."""
    op: str
    operand: 'ASTNode'
    
    def __repr__(self):
        return f"UnaryOpNode(op='{self.op}', operand={self.operand})"
    
    def to_dict(self):
        return {
            'type': 'UnaryOpNode',
            'op': self.op,
            'operand': self.operand.to_dict() if hasattr(self.operand, 'to_dict') else str(self.operand)
        }


@dataclass
class LiteralNode:
    """Represents a literal value."""
    value: Any
    
    def __repr__(self):
        return f"LiteralNode(value={repr(self.value)})"
    
    def to_dict(self):
        return {
            'type': 'LiteralNode',
            'value': self.value
        }


@dataclass
class IdentifierNode:
    """Represents an identifier (variable name)."""
    name: str
    
    def __repr__(self):
        return f"IdentifierNode(name='{self.name}')"
    
    def to_dict(self):
        return {
            'type': 'IdentifierNode',
            'name': self.name
        }


@dataclass
class ClassNode:
    """Represents a class definition."""
    name: str
    members_statements: List['ASTNode']
    
    def __repr__(self):
        return f"ClassNode(name='{self.name}', members={len(self.members_statements)})"
    
    def to_dict(self):
        return {
            'type': 'ClassNode',
            'name': self.name,
            'members': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.members_statements]
        }


@dataclass
class PrintNode:
    """Represents a print statement (convenience node)."""
    args: List['ASTNode']
    
    def __repr__(self):
        return f"PrintNode(args={len(self.args)})"
    
    def to_dict(self):
        return {
            'type': 'PrintNode',
            'args': [arg.to_dict() if hasattr(arg, 'to_dict') else str(arg) for arg in self.args]
        }


# Type alias for all AST nodes
ASTNode = Union[
    ProgramNode, FunctionNode, IfNode, LoopNode, AssignNode, CallNode,
    BinaryOpNode, UnaryOpNode, LiteralNode, IdentifierNode, ClassNode, PrintNode
]