"""
Parser module for the Lyric language.
Parses tokens into an Abstract Syntax Tree (AST).
"""

from typing import List, Optional, Union
from lyric.lexer import Token
from lyric.ast import (
    ProgramNode, FunctionNode, ClassNode, IfNode, ElifNode, LoopNode,
    AssignNode, CallNode, BinaryOpNode, UnaryOpNode, LiteralNode,
    IdentifierNode, PrintNode, ReturnNode
)
from lyric.errors import ParseError


class Parser:
    """Recursive descent parser for the Lyric language."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self) -> ProgramNode:
        """Parse tokens into a ProgramNode."""
        statements = []
        
        while not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        return ProgramNode(statements=statements)
    
    def _is_at_end(self) -> bool:
        """Check if we've consumed all tokens."""
        return self.pos >= len(self.tokens)
    
    def _peek(self) -> Optional[Token]:
        """Look at the current token without consuming it."""
        if self._is_at_end():
            return None
        return self.tokens[self.pos]
    
    def _advance(self) -> Optional[Token]:
        """Consume and return the current token."""
        if not self._is_at_end():
            self.pos += 1
        return self.tokens[self.pos - 1] if self.pos > 0 else None
    
    def _match(self, *token_types: str) -> bool:
        """Check if current token matches any of the given types."""
        if self._is_at_end():
            return False
        return self._peek().type in token_types
    
    def _consume(self, expected_type: str, message: str) -> Token:
        """Consume a token of expected type or raise error."""
        if self._match(expected_type):
            return self._advance()
        
        current = self._peek()
        if current is None:
            raise ParseError(f"{message} at end of file")
        else:
            raise ParseError(f"{message} at line {current.line}, col {current.col}")
    
    def _skip_newlines(self):
        """Skip newline tokens."""
        while self._match('NEWLINE'):
            self._advance()
    
    def _parse_statement(self) -> Optional[object]:
        """Parse a statement."""
        self._skip_newlines()
        
        if self._is_at_end():
            return None
        
        token = self._peek()
        
        if token.type == 'DEF':
            return self._parse_function_def()
        elif token.type == 'CLASS':
            return self._parse_class_def()
        elif token.type == 'IF':
            return self._parse_if_block()
        elif token.type == 'GIVEN':
            return self._parse_loop_block()
        elif token.type == 'RETURN':
            return self._parse_return_stmt()
        elif token.type == 'IDENTIFIER':
            # Could be assignment or expression statement
            return self._parse_assignment_or_expr_stmt()
        else:
            # This should not happen in well-formed code
            current = self._peek()
            raise ParseError(f"Unexpected token '{current.value}' at line {current.line}, col {current.col}")
    
    def _parse_function_def(self) -> FunctionNode:
        """Parse a function definition."""
        self._consume('DEF', "Expected 'def'")
        
        name_token = self._consume('IDENTIFIER', "Expected function name")
        name = name_token.value
        
        self._consume('LPAREN', "Expected '('")
        
        params = []
        if not self._match('RPAREN'):
            params = self._parse_param_list()
        
        self._consume('RPAREN', "Expected ')'")
        self._consume('LBRACE', "Expected '{'")
        
        # Parse body statements until closing brace
        body_statements = self._parse_function_body()
        
        self._consume('RBRACE', "Expected '}'")
        
        return FunctionNode(name=name, params=params, body_statements=body_statements)
    
    def _parse_function_body(self) -> List[object]:
        """Parse function body statements until closing brace."""
        statements = []
        
        while not self._is_at_end():
            # Skip newlines at the start
            self._skip_newlines()
            
            # Check if we've hit the closing brace
            if self._match('RBRACE'):
                break
                
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        return statements
    
    def _parse_class_def(self) -> ClassNode:
        """Parse a class definition."""
        self._consume('CLASS', "Expected 'class'")
        
        name_token = self._consume('IDENTIFIER', "Expected class name")
        name = name_token.value
        
        self._consume('COLON', "Expected ':'")
        self._skip_newlines()
        
        # Parse class members until CLASS_END
        members_statements = self._parse_class_body()
        
        self._consume('CLASS_END', "Expected '+++'")
        
        return ClassNode(name=name, members_statements=members_statements)
    
    def _parse_class_body(self) -> List[object]:
        """Parse class body statements until CLASS_END."""
        statements = []
        
        while not self._is_at_end():
            # Skip newlines at the start
            self._skip_newlines()
            
            # Check if we've hit the CLASS_END
            if self._match('CLASS_END'):
                break
                
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        return statements
    
    def _parse_if_block(self) -> IfNode:
        """Parse an if/else if/else block."""
        self._consume('IF', "Expected 'if'")
        
        condition = self._parse_expression()
        self._consume('COLON', "Expected ':' after if condition")
        
        then_body = self._parse_statement_list()
        
        elifs = []
        else_body = None
        
        # Parse elif clauses
        while self._match('ELSE'):
            self._advance()
            if self._match('IF'):
                # This is an elif
                self._advance()  # consume 'if'
                elif_condition = self._parse_expression()
                self._consume('COLON', "Expected ':' after elif condition")
                elif_body = self._parse_statement_list()
                elifs.append(ElifNode(condition=elif_condition, body=elif_body))
            else:
                # This is an else
                self._consume('COLON', "Expected ':' after else")
                else_body = self._parse_statement_list()
                break
        
        self._consume('END', "Expected 'end'")
        
        return IfNode(condition=condition, then_body=then_body, elifs=elifs, else_body=else_body)
    
    def _parse_loop_block(self) -> LoopNode:
        """Parse a given/done loop block."""
        self._consume('GIVEN', "Expected 'given'")
        
        condition_or_iter = self._parse_expression()
        self._consume('COLON', "Expected ':' after given expression")
        
        body = self._parse_statement_list()
        
        self._consume('DONE', "Expected 'done'")
        
        # Determine loop kind based on the expression
        loop_kind = "iterator" if self._is_iterator_expression(condition_or_iter) else "while"
        
        return LoopNode(condition_or_iter=condition_or_iter, loop_kind=loop_kind, body=body)
    
    def _is_iterator_expression(self, expr) -> bool:
        """Check if expression is an iterator (e.g., 'i in range(5)')."""
        if isinstance(expr, BinaryOpNode) and expr.op == "in":
            return True
        return False
    
    def _parse_assignment_or_expr_stmt(self) -> object:
        """Parse assignment or expression statement."""
        # Look ahead to see if this is an assignment
        if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == 'ASSIGN':
            # This is an assignment
            name_token = self._consume('IDENTIFIER', "Expected identifier")
            self._advance()  # consume '='
            expr = self._parse_expression()
            return AssignNode(name=name_token.value, expr=expr)
        else:
            # This is an expression statement
            return self._parse_expression()
    
    def _parse_statement_list(self) -> List[object]:
        """Parse a list of statements until end marker."""
        statements = []
        
        while not self._is_at_end():
            # Skip newlines at the start
            self._skip_newlines()
            
            # Check if we've hit an end marker
            if self._match('END', 'DONE', 'RBRACE', 'CLASS_END'):
                break
            
            # Check if we've hit control flow keywords that end statement lists
            if self._match('ELSE'):
                break
                
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        return statements
    
    def _parse_param_list(self) -> List[str]:
        """Parse parameter list."""
        params = []
        
        while True:
            param_token = self._consume('IDENTIFIER', "Expected parameter name")
            params.append(param_token.value)
            
            if self._match('COMMA'):
                self._advance()
            else:
                break
        
        return params
    
    def _parse_expression(self) -> object:
        """Parse an expression."""
        return self._parse_logical_or()
    
    def _parse_logical_or(self) -> object:
        """Parse logical OR expressions."""
        expr = self._parse_logical_and()
        
        while self._match('OR'):
            op_token = self._advance()
            right = self._parse_logical_and()
            expr = BinaryOpNode(op=op_token.value, left=expr, right=right)
        
        return expr
    
    def _parse_logical_and(self) -> object:
        """Parse logical AND expressions."""
        expr = self._parse_equality()
        
        while self._match('AND'):
            op_token = self._advance()
            right = self._parse_equality()
            expr = BinaryOpNode(op=op_token.value, left=expr, right=right)
        
        return expr
    
    def _parse_equality(self) -> object:
        """Parse equality expressions."""
        expr = self._parse_comparison()
        
        while self._match('EQ', 'NE'):
            op_token = self._advance()
            right = self._parse_comparison()
            expr = BinaryOpNode(op=op_token.value, left=expr, right=right)
        
        return expr
    
    def _parse_comparison(self) -> object:
        """Parse comparison expressions."""
        expr = self._parse_term()
        
        while self._match('GT', 'GE', 'LT', 'LE', 'IN'):
            op_token = self._advance()
            right = self._parse_term()
            expr = BinaryOpNode(op=op_token.value, left=expr, right=right)
        
        return expr
    
    def _parse_term(self) -> object:
        """Parse addition and subtraction."""
        expr = self._parse_factor()
        
        while self._match('PLUS', 'MINUS'):
            op_token = self._advance()
            right = self._parse_factor()
            expr = BinaryOpNode(op=op_token.value, left=expr, right=right)
        
        return expr
    
    def _parse_factor(self) -> object:
        """Parse multiplication, division, and modulo."""
        expr = self._parse_unary()
        
        while self._match('MULTIPLY', 'DIVIDE', 'MODULO'):
            op_token = self._advance()
            right = self._parse_unary()
            expr = BinaryOpNode(op=op_token.value, left=expr, right=right)
        
        return expr
    
    def _parse_unary(self) -> object:
        """Parse unary expressions."""
        if self._match('NOT', 'MINUS', 'PLUS'):
            op_token = self._advance()
            operand = self._parse_unary()
            return UnaryOpNode(op=op_token.value, operand=operand)
        
        return self._parse_primary()
    
    def _parse_primary(self) -> object:
        """Parse primary expressions."""
        if self._match('FALSE'):
            self._advance()
            return LiteralNode(False)
        elif self._match('TRUE'):
            self._advance()
            return LiteralNode(True)
        elif self._match('INTEGER'):
            token = self._advance()
            return LiteralNode(int(token.value))
        elif self._match('FLOAT'):
            token = self._advance()
            return LiteralNode(float(token.value))
        elif self._match('STRING'):
            token = self._advance()
            # Remove quotes from string
            return LiteralNode(token.value[1:-1])
        elif self._match('IDENTIFIER'):
            token = self._advance()
            
            # Check if this is a function call
            if self._match('LPAREN'):
                return self._parse_call(token.value)
            else:
                expr = IdentifierNode(token.value)
                # Handle member access (e.g., self.name)
                while self._match('DOT'):
                    self._advance()  # consume '.'
                    member_token = self._consume('IDENTIFIER', "Expected member name after '.'")
                    # For now, we'll create a simple identifier with the full name
                    # In a more sophisticated parser, this would be a MemberAccessNode
                    expr = IdentifierNode(f"{expr.name}.{member_token.value}")
                return expr
        elif self._match('LPAREN'):
            self._advance()  # consume '('
            expr = self._parse_expression()
            self._consume('RPAREN', "Expected ')' after expression")
            return expr
        else:
            current = self._peek()
            raise ParseError(f"Unexpected token '{current.value}' at line {current.line}, col {current.col}")
    
    def _parse_call(self, func_name: str) -> CallNode:
        """Parse a function call."""
        self._consume('LPAREN', "Expected '('")
        
        args = []
        if not self._match('RPAREN'):
            args = self._parse_arg_list()
        
        self._consume('RPAREN', "Expected ')'")
        
        return CallNode(func_name=func_name, args=args)
    
    def _parse_arg_list(self) -> List[object]:
        """Parse argument list."""
        args = []
        
        while True:
            args.append(self._parse_expression())
            
            if self._match('COMMA'):
                self._advance()
            else:
                break
        
        return args
    
    def _parse_return_stmt(self) -> 'ReturnNode':
        """Parse a return statement."""
        self._consume('RETURN', "Expected 'return'")
        
        # Check if there's an expression
        expr = None
        if not self._match('NEWLINE', 'END', 'DONE', 'RBRACE', 'CLASS_END'):
            expr = self._parse_expression()
        
        return ReturnNode(expr=expr)


def parse(source: str) -> ProgramNode:
    """Parse source code into a ProgramNode.
    
    Args:
        source: The source code to parse
        
    Returns:
        ProgramNode representing the parsed program
    """
    from lyric.lexer import tokenize
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse()
