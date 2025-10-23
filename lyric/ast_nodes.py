"""AST node definitions for Lyric language."""

from dataclasses import dataclass
from typing import List, Optional, Any, Union


class ASTNode:
    """Base class for all AST nodes with position tracking."""
    
    def get_position(self) -> tuple[int, int]:
        """Get the line and column position of this node."""
        return (getattr(self, 'line', 0), getattr(self, 'column', 0))


@dataclass
class ProgramNode(ASTNode):
    """Represents the root of a Lyric program."""
    statements: List['ASTNode']
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"ProgramNode(statements={len(self.statements)})"
    
    def to_dict(self):
        return {
            'type': 'ProgramNode',
            'statements': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.statements]
        }


@dataclass
class FunctionNode(ASTNode):
    """Represents a function definition."""
    name: str
    params: List[str]
    param_types: Optional[List[str]] = None  # Optional list of parameter types
    body_statements: List['ASTNode'] = None
    line: int = 0
    column: int = 0
    
    def __post_init__(self):
        if self.body_statements is None:
            self.body_statements = []
        if self.param_types is None:
            self.param_types = []
    
    def __repr__(self):
        return f"FunctionNode(name='{self.name}', params={self.params}, param_types={self.param_types}, body={len(self.body_statements)})"
    
    def to_dict(self):
        return {
            'type': 'FunctionNode',
            'name': self.name,
            'params': self.params,
            'param_types': self.param_types,
            'body': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.body_statements]
        }


@dataclass
class IfNode(ASTNode):
    """Represents an if/elif/else statement."""
    condition: 'ASTNode'
    then_body: List['ASTNode']
    elifs: List[tuple['ASTNode', List['ASTNode']]]  # List of (condition, body) tuples
    else_body: Optional[List['ASTNode']]
    line: int = 0
    column: int = 0
    
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
class LoopNode(ASTNode):
    """Represents a loop statement (given/done)."""
    condition_or_iter: 'ASTNode'
    loop_kind: str  # "iterator" or "while"
    body: List['ASTNode']
    iterator_var: Optional[str] = None  # Variable name for iterator loops
    line: int = 0
    column: int = 0
    
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
class AssignNode(ASTNode):
    """Represents a variable assignment."""
    name: str
    expr: 'ASTNode'
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"AssignNode(name='{self.name}', expr={self.expr})"
    
    def to_dict(self):
        return {
            'type': 'AssignNode',
            'name': self.name,
            'expr': self.expr.to_dict() if hasattr(self.expr, 'to_dict') else str(self.expr)
        }


@dataclass
class CallNode(ASTNode):
    """Represents a function call."""
    func_name: str
    args: List['ASTNode']
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"CallNode(func='{self.func_name}', args={len(self.args)})"
    
    def to_dict(self):
        return {
            'type': 'CallNode',
            'func_name': self.func_name,
            'args': [arg.to_dict() if hasattr(arg, 'to_dict') else str(arg) for arg in self.args]
        }


@dataclass
class BinaryOpNode(ASTNode):
    """Represents a binary operation."""
    op: str
    left: 'ASTNode'
    right: 'ASTNode'
    line: int = 0
    column: int = 0
    
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
class UnaryOpNode(ASTNode):
    """Represents a unary operation."""
    op: str
    operand: 'ASTNode'
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"UnaryOpNode(op='{self.op}', operand={self.operand})"
    
    def to_dict(self):
        return {
            'type': 'UnaryOpNode',
            'op': self.op,
            'operand': self.operand.to_dict() if hasattr(self.operand, 'to_dict') else str(self.operand)
        }


@dataclass
class LiteralNode(ASTNode):
    """Represents a literal value."""
    value: Any
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"LiteralNode(value={repr(self.value)})"
    
    def to_dict(self):
        return {
            'type': 'LiteralNode',
            'value': self.value
        }


@dataclass
class IdentifierNode(ASTNode):
    """Represents an identifier (variable name)."""
    name: str
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"IdentifierNode(name='{self.name}')"
    
    def to_dict(self):
        return {
            'type': 'IdentifierNode',
            'name': self.name
        }


@dataclass
class ClassNode(ASTNode):
    """Represents a class definition."""
    name: str
    members_statements: List['ASTNode']
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"ClassNode(name='{self.name}', members={len(self.members_statements)})"
    
    def to_dict(self):
        return {
            'type': 'ClassNode',
            'name': self.name,
            'members': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.members_statements]
        }


@dataclass
class ReturnNode(ASTNode):
    """Represents a return statement."""
    value: Optional['ASTNode']
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"ReturnNode(value={self.value})"
    
    def to_dict(self):
        return {
            'type': 'ReturnNode',
            'value': self.value.to_dict() if self.value and hasattr(self.value, 'to_dict') else str(self.value)
        }


@dataclass
class ListLiteralNode(ASTNode):
    """Represents a list literal."""
    elements: List['ASTNode']
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"ListLiteralNode(elements={len(self.elements)})"
    
    def to_dict(self):
        return {
            'type': 'ListLiteralNode',
            'elements': [elem.to_dict() if hasattr(elem, 'to_dict') else str(elem) for elem in self.elements]
        }


@dataclass
class DictLiteralNode(ASTNode):
    """Represents a dictionary literal."""
    pairs: List[tuple['ASTNode', 'ASTNode']]  # List of (key, value) pairs
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"DictLiteralNode(pairs={len(self.pairs)})"
    
    def to_dict(self):
        return {
            'type': 'DictLiteralNode',
            'pairs': [(key.to_dict() if hasattr(key, 'to_dict') else str(key),
                      value.to_dict() if hasattr(value, 'to_dict') else str(value))
                     for key, value in self.pairs]
        }


@dataclass
class IndexNode(ASTNode):
    """Represents an indexing operation (list[index] or dict[key])."""
    obj: 'ASTNode'  # The object being indexed
    index: 'ASTNode'  # The index/key
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"IndexNode(obj={self.obj}, index={self.index})"
    
    def to_dict(self):
        return {
            'type': 'IndexNode',
            'obj': self.obj.to_dict() if hasattr(self.obj, 'to_dict') else str(self.obj),
            'index': self.index.to_dict() if hasattr(self.index, 'to_dict') else str(self.index)
        }


@dataclass
class TypeDeclarationNode(ASTNode):
    """Represents a typed variable declaration."""
    type_name: str
    name: str
    expr: 'ASTNode'
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"TypeDeclarationNode(type='{self.type_name}', name='{self.name}', expr={self.expr})"
    
    def to_dict(self):
        return {
            'type': 'TypeDeclarationNode',
            'type_name': self.type_name,
            'name': self.name,
            'expr': self.expr.to_dict() if hasattr(self.expr, 'to_dict') else str(self.expr)
        }


@dataclass
class PrintNode(ASTNode):
    """Represents a print statement (convenience node)."""
    args: List['ASTNode']
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"PrintNode(args={len(self.args)})"
    
    def to_dict(self):
        return {
            'type': 'PrintNode',
            'args': [arg.to_dict() if hasattr(arg, 'to_dict') else str(arg) for arg in self.args]
        }


@dataclass
class TryNode(ASTNode):
    """Represents a try/catch/finally statement."""
    try_body: List['ASTNode']
    catch_body: Optional[List['ASTNode']]
    finally_body: Optional[List['ASTNode']]
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        catch_present = self.catch_body is not None
        finally_present = self.finally_body is not None
        return f"TryNode(try={len(self.try_body)}, catch={catch_present}, finally={finally_present})"
    
    def to_dict(self):
        return {
            'type': 'TryNode',
            'try_body': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.try_body],
            'catch_body': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.catch_body] if self.catch_body else None,
            'finally_body': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.finally_body] if self.finally_body else None
        }


@dataclass
class RaiseNode(ASTNode):
    """Represents a raise statement."""
    exception_name: str
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"RaiseNode(exception='{self.exception_name}')"
    
    def to_dict(self):
        return {
            'type': 'RaiseNode',
            'exception_name': self.exception_name
        }


@dataclass
class MultiDeclarationNode(ASTNode):
    """Represents multiple variable declarations in a single line."""
    declarations: List[tuple[str, str]]  # List of (type_name, variable_name) tuples
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"MultiDeclarationNode(declarations={self.declarations})"
    
    def to_dict(self):
        return {
            'type': 'MultiDeclarationNode',
            'declarations': self.declarations
        }


@dataclass
class ImportPyNode(ASTNode):
    """Represents an importpy statement."""
    module_name: str
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"ImportPyNode(module='{self.module_name}')"
    
    def to_dict(self):
        return {
            'type': 'ImportPyNode',
            'module_name': self.module_name
        }


# Type alias for all AST nodes
ASTNode = Union[
    ProgramNode, FunctionNode, IfNode, LoopNode, AssignNode, CallNode,
    BinaryOpNode, UnaryOpNode, LiteralNode, IdentifierNode, ClassNode, ReturnNode, 
    ListLiteralNode, DictLiteralNode, IndexNode, TypeDeclarationNode, MultiDeclarationNode, PrintNode,
    TryNode, RaiseNode, ImportPyNode
]