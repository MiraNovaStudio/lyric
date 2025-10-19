"""
Lyric Language AST (Abstract Syntax Tree) Nodes
Defines node types for syntax trees.
"""


class ASTNode:
    """Base class for all AST nodes."""
    pass


class ProgramNode(ASTNode):
    """Represents a complete program."""
    
    def __init__(self, statements):
        self.statements = statements
    
    def __repr__(self):
        return f"ProgramNode({self.statements})"


class FunctionNode(ASTNode):
    """Represents a function definition."""
    
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
    
    def __repr__(self):
        return f"FunctionNode({self.name}, {self.params}, {self.body})"


class IfNode(ASTNode):
    """Represents an if statement."""
    
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body
    
    def __repr__(self):
        return f"IfNode({self.condition}, {self.then_body}, {self.else_body})"


class GivenNode(ASTNode):
    """Represents a given loop."""
    
    def __init__(self, variable, iterable, body):
        self.variable = variable
        self.iterable = iterable
        self.body = body
    
    def __repr__(self):
        return f"GivenNode({self.variable}, {self.iterable}, {self.body})"


class AssignmentNode(ASTNode):
    """Represents a variable assignment."""
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def __repr__(self):
        return f"AssignmentNode({self.name}, {self.value})"


class BinaryOpNode(ASTNode):
    """Represents a binary operation."""
    
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __repr__(self):
        return f"BinaryOpNode({self.left}, {self.op}, {self.right})"


class UnaryOpNode(ASTNode):
    """Represents a unary operation."""
    
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand
    
    def __repr__(self):
        return f"UnaryOpNode({self.op}, {self.operand})"


class VariableNode(ASTNode):
    """Represents a variable reference."""
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"VariableNode({self.name})"


class LiteralNode(ASTNode):
    """Represents a literal value."""
    
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"LiteralNode({self.value})"


class FunctionCallNode(ASTNode):
    """Represents a function call."""
    
    def __init__(self, name, args):
        self.name = name
        self.args = args
    
    def __repr__(self):
        return f"FunctionCallNode({self.name}, {self.args})"


class BlockNode(ASTNode):
    """Represents a block of statements."""
    
    def __init__(self, statements):
        self.statements = statements
    
    def __repr__(self):
        return f"BlockNode({self.statements})"
