"""
AST (Abstract Syntax Tree) definitions for the Lyric language.
Contains node classes for the language constructs.
"""

from dataclasses import dataclass
from typing import List, Optional, Union, Any


@dataclass
class ASTNode:
    """Base class for all AST nodes."""

    def to_dict(self) -> dict:
        """Convert node to dictionary representation for debugging."""
        result = {}
        for field_name, field_value in self.__dict__.items():
            if isinstance(field_value, list):
                result[field_name] = [
                    item.to_dict() if hasattr(item, 'to_dict') else item
                    for item in field_value
                ]
            elif hasattr(field_value, 'to_dict'):
                result[field_name] = field_value.to_dict()
            else:
                result[field_name] = field_value
        return result


@dataclass
class ProgramNode(ASTNode):
    """Represents the root of a program."""
    statements: List[ASTNode]

    def __repr__(self):
        return f"ProgramNode(statements={len(self.statements)} items)"


@dataclass
class FunctionNode(ASTNode):
    """Represents a function definition."""
    name: str
    params: List[str]
    body_statements: List[ASTNode]

    def __repr__(self):
        return (f"FunctionNode(name='{self.name}', params={self.params}, "
                f"body={len(self.body_statements)} statements)")


@dataclass
class IfNode(ASTNode):
    """Represents an if/else if/else statement."""
    condition: ASTNode
    then_body: List[ASTNode]
    elifs: List['ElifNode']
    else_body: Optional[List[ASTNode]]

    def __repr__(self):
        else_info = f", else={len(self.else_body)} statements" if self.else_body else ""
        return (f"IfNode(condition={self.condition}, then={len(self.then_body)} statements, "
                f"elifs={len(self.elifs)}{else_info})")


@dataclass
class ElifNode(ASTNode):
    """Represents an elif clause."""
    condition: ASTNode
    body: List[ASTNode]

    def __repr__(self):
        return f"ElifNode(condition={self.condition}, body={len(self.body)} statements)"


@dataclass
class LoopNode(ASTNode):
    """Represents a loop (given/done construct)."""
    condition_or_iter: ASTNode
    loop_kind: str  # "iterator" or "while"
    body: List[ASTNode]

    def __repr__(self):
        return (f"LoopNode(kind='{self.loop_kind}', condition={self.condition_or_iter}, "
                f"body={len(self.body)} statements)")


@dataclass
class AssignNode(ASTNode):
    """Represents a variable assignment."""
    name: Union[str, ASTNode]  # Can be string (simple var) or ASTNode
    expr: ASTNode

    def __repr__(self):
        return f"AssignNode(name={self.name}, expr={self.expr})"


@dataclass
class CallNode(ASTNode):
    """Represents a function call."""
    func_name: str
    args: List[ASTNode]

    def __repr__(self):
        return f"CallNode(func='{self.func_name}', args={len(self.args)} items)"


@dataclass
class MethodCallNode(ASTNode):
    """Represents a method call (object.method())."""
    object: ASTNode
    method: str
    args: List[ASTNode]

    def __repr__(self):
        return (f"MethodCallNode(object={self.object}, method='{self.method}', "
                f"args={len(self.args)} items)")


@dataclass
class BinaryOpNode(ASTNode):
    """Represents a binary operation."""
    op: str
    left: ASTNode
    right: ASTNode

    def __repr__(self):
        return f"BinaryOpNode(op='{self.op}', left={self.left}, right={self.right})"


@dataclass
class UnaryOpNode(ASTNode):
    """Represents a unary operation."""
    op: str
    operand: ASTNode

    def __repr__(self):
        return f"UnaryOpNode(op='{self.op}', operand={self.operand})"


@dataclass
class LiteralNode(ASTNode):
    """Represents a literal value."""
    value: Any

    def __repr__(self):
        return f"LiteralNode(value={repr(self.value)})"


@dataclass
class IdentifierNode(ASTNode):
    """Represents an identifier."""
    name: str

    def __repr__(self):
        return f"IdentifierNode(name='{self.name}')"


@dataclass
class MemberAccessNode(ASTNode):
    """Represents member access (object.attribute or object.method)."""
    object: ASTNode
    member: str

    def __repr__(self):
        return f"MemberAccessNode(object={self.object}, member='{self.member}')"


@dataclass
class ClassNode(ASTNode):
    """Represents a class definition."""
    name: str
    members_statements: List[ASTNode]

    def __repr__(self):
        return f"ClassNode(name='{self.name}', members={len(self.members_statements)} items)"


@dataclass
class PrintNode(ASTNode):
    """Represents a print statement (convenience node)."""
    args: List[ASTNode]

    def __repr__(self):
        return f"PrintNode(args={len(self.args)} items)"


@dataclass
class ImportNode(ASTNode):
    """Represents an import statement."""
    module: str
    alias: Optional[str] = None
    items: Optional[List[str]] = None

    def __repr__(self):
        if self.items:
            return f"ImportNode(module='{self.module}', items={self.items})"
        elif self.alias:
            return f"ImportNode(module='{self.module}', alias='{self.alias}')"
        else:
            return f"ImportNode(module='{self.module}')"


@dataclass
class ReturnNode(ASTNode):
    """Represents a return statement."""
    expr: Optional[ASTNode] = None

    def __repr__(self):
        return f"ReturnNode(expr={self.expr})"


@dataclass
class TryNode(ASTNode):
    """Represents a try/except/finally block."""
    try_body: List[ASTNode]
    except_clauses: List['ExceptNode']
    finally_body: Optional[List[ASTNode]]

    def __repr__(self):
        finally_info = f", finally={len(self.finally_body)} statements" if self.finally_body else ""
        return (f"TryNode(try={len(self.try_body)} statements, "
                f"excepts={len(self.except_clauses)}{finally_info})")


@dataclass
class ExceptNode(ASTNode):
    """Represents an except clause."""
    exception_type: Optional[str]
    body: List[ASTNode]

    def __repr__(self):
        return f"ExceptNode(type='{self.exception_type}', body={len(self.body)} statements)"


# Update the forward reference for ElifNode
IfNode.__annotations__['elifs'] = List[ElifNode]
