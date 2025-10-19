"""
Lyric Language Parser
Builds the abstract syntax tree from tokens.
"""

from lyric.lexer import Token
from lyric.ast import *
from lyric.errors import ParseError


class Parser:
    """Parser for the Lyric language."""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None
    
    def parse(self):
        """Parse tokens into an AST."""
        statements = []
        
        while self.current_token and self.current_token.type != 'EOF':
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        return ProgramNode(statements)
    
    def _parse_statement(self):
        """Parse a single statement."""
        if not self.current_token:
            return None
        
        if self.current_token.type == 'DEF':
            return self._parse_function()
        elif self.current_token.type == 'IF':
            return self._parse_if()
        elif self.current_token.type == 'GIVEN':
            return self._parse_given()
        elif self.current_token.type == 'END':
            self._advance()
            return None  # End marker
        elif self.current_token.type == 'DONE':
            self._advance()
            return None  # Done marker
        elif self.current_token.type == 'ELSE':
            self._advance()
            return None  # Else marker
        elif self.current_token.type == 'IDENTIFIER':
            return self._parse_assignment_or_call()
        
        return None
    
    def _parse_function(self):
        """Parse a function definition."""
        self._advance()  # Skip DEF token
        
        if self.current_token.type != 'IDENTIFIER':
            raise ParseError(f"Expected function name at line {self.current_token.line}")
        
        name = self.current_token.value
        self._advance()
        
        # Parse parameters
        params = []
        if self.current_token.type == 'LPAREN':
            self._advance()
            while self.current_token.type != 'RPAREN':
                if self.current_token.type == 'IDENTIFIER':
                    params.append(self.current_token.value)
                    self._advance()
                if self.current_token.type == 'COMMA':
                    self._advance()
            self._advance()  # Skip ')'
        
        # Parse body
        if self.current_token.type != 'LBRACE':
            raise ParseError(f"Expected '{{' at line {self.current_token.line}")
        
        self._advance()  # Skip '{'
        body = self._parse_block()
        
        if self.current_token.type != 'RBRACE':
            raise ParseError(f"Expected '}}' at line {self.current_token.line}")
        
        self._advance()  # Skip '}'
        
        return FunctionNode(name, params, body)
    
    def _parse_if(self):
        """Parse an if statement."""
        self._advance()  # Skip IF token
        
        condition = self._parse_expression()
        
        if self.current_token.type != 'COLON':
            raise ParseError(f"Expected ':' at line {self.current_token.line}")
        
        self._advance()  # Skip ':'
        
        then_body = self._parse_block()
        
        # Check for else
        else_body = None
        if self.current_token and self.current_token.type == 'ELSE':
            self._advance()  # Skip ELSE token
            if self.current_token.type == 'COLON':
                self._advance()  # Skip ':'
                else_body = self._parse_block()
        
        # Expect 'end'
        if not self.current_token or self.current_token.type != 'END':
            raise ParseError(f"Expected 'end' at line {self.current_token.line}")
        
        self._advance()  # Skip END token
        
        return IfNode(condition, then_body, else_body)
    
    def _parse_given(self):
        """Parse a given loop."""
        self._advance()  # Skip GIVEN token
        
        if self.current_token.type != 'IDENTIFIER':
            raise ParseError(f"Expected variable name at line {self.current_token.line}")
        
        variable = self.current_token.value
        self._advance()
        
        if self.current_token.type != 'IN':
            raise ParseError(f"Expected 'in' at line {self.current_token.line}")
        
        self._advance()  # Skip IN token
        
        iterable = self._parse_expression()
        
        if self.current_token.type != 'COLON':
            raise ParseError(f"Expected ':' at line {self.current_token.line}")
        
        self._advance()  # Skip ':'
        
        body = self._parse_block()
        
        # Expect 'done'
        if not self.current_token or self.current_token.type != 'DONE':
            raise ParseError(f"Expected 'done' at line {self.current_token.line}")
        
        self._advance()  # Skip DONE token
        
        return GivenNode(variable, iterable, body)
    
    def _parse_assignment_or_call(self):
        """Parse assignment or function call."""
        name = self.current_token.value
        self._advance()
        
        if self.current_token.type == 'ASSIGN':
            self._advance()  # Skip '='
            value = self._parse_expression()
            return AssignmentNode(name, value)
        elif self.current_token.type == 'LPAREN':
            # Function call
            self._advance()  # Skip '('
            args = []
            while self.current_token.type != 'RPAREN':
                args.append(self._parse_expression())
                if self.current_token.type == 'COMMA':
                    self._advance()
            self._advance()  # Skip ')'
            return FunctionCallNode(name, args)
        
        return None
    
    def _parse_expression(self):
        """Parse an expression."""
        return self._parse_logical_or()
    
    def _parse_logical_or(self):
        """Parse logical OR expression."""
        left = self._parse_logical_and()
        
        while self.current_token and self.current_token.type == 'OR':
            op = self.current_token.value
            self._advance()
            right = self._parse_logical_and()
            left = BinaryOpNode(left, op, right)
        
        return left
    
    def _parse_logical_and(self):
        """Parse logical AND expression."""
        left = self._parse_equality()
        
        while self.current_token and self.current_token.type == 'AND':
            op = self.current_token.value
            self._advance()
            right = self._parse_equality()
            left = BinaryOpNode(left, op, right)
        
        return left
    
    def _parse_equality(self):
        """Parse equality expression."""
        left = self._parse_comparison()
        
        while self.current_token and self.current_token.type in ('EQUAL', 'NOTEQUAL'):
            op = self.current_token.type
            self._advance()
            right = self._parse_comparison()
            left = BinaryOpNode(left, op, right)
        
        return left
    
    def _parse_comparison(self):
        """Parse comparison expression."""
        left = self._parse_term()
        
        while self.current_token and self.current_token.type in ('LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL'):
            op = self.current_token.type
            self._advance()
            right = self._parse_term()
            left = BinaryOpNode(left, op, right)
        
        return left
    
    def _parse_term(self):
        """Parse addition/subtraction."""
        left = self._parse_factor()
        
        while self.current_token and self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token.type
            self._advance()
            right = self._parse_factor()
            left = BinaryOpNode(left, op, right)
        
        return left
    
    def _parse_factor(self):
        """Parse multiplication/division."""
        left = self._parse_unary()
        
        while self.current_token and self.current_token.type in ('MULTIPLY', 'DIVIDE'):
            op = self.current_token.type
            self._advance()
            right = self._parse_unary()
            left = BinaryOpNode(left, op, right)
        
        return left
    
    def _parse_unary(self):
        """Parse unary operations."""
        if self.current_token and self.current_token.type == 'NOT':
            op = self.current_token.value
            self._advance()
            operand = self._parse_unary()
            return UnaryOpNode(op, operand)
        
        return self._parse_primary()
    
    def _parse_primary(self):
        """Parse primary expressions."""
        if self.current_token.type == 'NUMBER':
            value = float(self.current_token.value) if '.' in self.current_token.value else int(self.current_token.value)
            self._advance()
            return LiteralNode(value)
        
        elif self.current_token.type == 'STRING':
            value = self.current_token.value[1:-1]  # Remove quotes
            self._advance()
            return LiteralNode(value)
        
        elif self.current_token.type == 'IDENTIFIER':
            name = self.current_token.value
            self._advance()
            return VariableNode(name)
        
        elif self.current_token.type == 'LPAREN':
            self._advance()
            expr = self._parse_expression()
            if self.current_token.type != 'RPAREN':
                raise ParseError(f"Expected ')' at line {self.current_token.line}")
            self._advance()
            return expr
        
        raise ParseError(f"Unexpected token {self.current_token.type} at line {self.current_token.line}")
    
    def _parse_block(self):
        """Parse a block of statements."""
        statements = []
        
        while self.current_token and self.current_token.type != 'EOF':
            if self.current_token.type in ('END', 'DONE', 'ELSE'):
                break
            
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        return BlockNode(statements)
    
    def _advance(self):
        """Advance to the next token."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
