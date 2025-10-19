"""Parser module for converting tokens to AST."""

from typing import List
from lyric.lexer import Token, tokenize
from lyric.ast_nodes import (
    ProgramNode, FunctionNode, IfNode, LoopNode, AssignNode, CallNode,
    BinaryOpNode, UnaryOpNode, LiteralNode, IdentifierNode, ClassNode, ReturnNode, ListLiteralNode
)
from lyric.errors import ParseError, SyntaxErrorLyric


class Parser:
    """Recursive descent parser for Lyric language."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
    
    def parse(self) -> ProgramNode:
        """Parse tokens into a ProgramNode."""
        statements = []
        
        while not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        return ProgramNode(statements)
    
    def _is_at_end(self) -> bool:
        """Check if we've reached the end of tokens."""
        return (self.current >= len(self.tokens) or 
                (self.current < len(self.tokens) and 
                 self.tokens[self.current].type == 'EOF'))
    
    def _peek(self) -> Token:
        """Look at the current token without advancing."""
        if self.current >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[self.current]
    
    def _advance(self) -> Token:
        """Advance to the next token and return the previous one."""
        if not self._is_at_end():
            self.current += 1
        return self.tokens[self.current - 1]
    
    def _check(self, *token_types: str) -> bool:
        """Check if current token matches any of the given types."""
        if self._is_at_end():
            return False
        return self._peek().type in token_types
    
    def _match(self, *token_types: str) -> bool:
        """Match and consume current token if it matches any of the given types."""
        if self._check(*token_types):
            self._advance()
            return True
        return False
    
    def _consume(self, token_type: str, message: str) -> Token:
        """Consume token of expected type or raise ParseError."""
        if self._check(token_type):
            return self._advance()
        raise ParseError(f"{message} at line {self._peek().line}, column {self._peek().col}")
    
    def _parse_statement(self):
        """Parse a single statement."""
        # Skip NEWLINE tokens
        while self._match('NEWLINE'):
            pass
        
        # If we're at EOF after skipping newlines, return None
        if self._is_at_end():
            return None
        
        if self._check('DEF'):
            return self._parse_func_def()
        elif self._check('CLASS'):
            return self._parse_class_def()
        elif self._check('IF'):
            return self._parse_if_block()
        elif self._check('GIVEN'):
            return self._parse_loop_block()
        elif self._check('RETURN'):
            return self._parse_return_stmt()
        else:
            return self._parse_assignment_or_expr_stmt()
    
    def _parse_func_def(self) -> FunctionNode:
        """Parse function definition: def IDENT "(" param_list? ")" "{" statement* "}" """
        self._consume('DEF', "Expected 'def'")
        
        name_token = self._consume('IDENT', "Expected function name")
        name = name_token.value
        
        self._consume('LPAREN', "Expected '(' after function name")
        
        params = []
        if not self._check('RPAREN'):
            params = self._parse_param_list()
        
        self._consume('RPAREN', "Expected ')' after parameters")
        self._consume('LBRACE', "Expected '{' after function signature")
        
        body_statements = []
        while not self._check('RBRACE') and not self._is_at_end():
            # Skip NEWLINE tokens
            while self._match('NEWLINE'):
                pass
            
            if self._check('RBRACE'):
                break
                
            stmt = self._parse_statement()
            if stmt:
                body_statements.append(stmt)
        
        self._consume('RBRACE', "Expected '}' after function body")
        
        return FunctionNode(name, params, body_statements)
    
    def _parse_param_list(self) -> List[str]:
        """Parse parameter list: IDENT ("," IDENT)*"""
        params = []
        
        if self._check('IDENT'):
            param_token = self._advance()
            params.append(param_token.value)
            
            while self._match('COMMA'):
                if self._check('IDENT'):
                    param_token = self._advance()
                    params.append(param_token.value)
                else:
                    raise ParseError(
                        f"Expected parameter name after ',' at line {self._peek().line}, "
                        f"column {self._peek().col}")
        
        return params
    
    def _parse_class_def(self) -> ClassNode:
        """Parse class definition: class IDENT ":" statement* CLASS_END"""
        self._consume('CLASS', "Expected 'class'")
        
        name_token = self._consume('IDENT', "Expected class name")
        name = name_token.value
        
        self._consume('COLON', "Expected ':' after class name")
        
        members_statements = []
        while not self._check('CLASS_END') and not self._is_at_end():
            # Skip NEWLINE tokens
            while self._match('NEWLINE'):
                pass
            
            if self._check('CLASS_END'):
                break
                
            stmt = self._parse_statement()
            if stmt:
                members_statements.append(stmt)
        
        self._consume('CLASS_END', "Expected '+++' after class body")
        
        return ClassNode(name, members_statements)
    
    def _parse_if_block(self) -> IfNode:
        """Parse if block: if expression ":" statement* ("else" "if" expression ":" statement*)* ("else" ":" statement*)? "end" """
        self._consume('IF', "Expected 'if'")
        
        condition = self._parse_expression()
        self._consume('COLON', "Expected ':' after if condition")
        
        then_body = []
        while not self._check('ELSE', 'END') and not self._is_at_end():
            # Skip NEWLINE tokens
            while self._match('NEWLINE'):
                pass
            
            if self._check('ELSE', 'END'):
                break
                
            stmt = self._parse_statement()
            if stmt:
                then_body.append(stmt)
        
        elifs = []
        else_body = None
        
        while self._match('ELSE'):
            if self._match('IF'):
                # elif clause
                elif_condition = self._parse_expression()
                self._consume('COLON', "Expected ':' after elif condition")
                
                elif_body = []
                while not self._check('ELSE', 'END') and not self._is_at_end():
                    # Skip NEWLINE tokens
                    while self._match('NEWLINE'):
                        pass
                    
                    if self._check('ELSE', 'END'):
                        break
                        
                    stmt = self._parse_statement()
                    if stmt:
                        elif_body.append(stmt)
                
                elifs.append((elif_condition, elif_body))
            else:
                # else clause
                self._consume('COLON', "Expected ':' after else")
                
                else_body = []
                while not self._check('END') and not self._is_at_end():
                    # Skip NEWLINE tokens
                    while self._match('NEWLINE'):
                        pass
                    
                    if self._check('END'):
                        break
                        
                    stmt = self._parse_statement()
                    if stmt:
                        else_body.append(stmt)
                break
        
        self._consume('END', "Expected 'end' after if block")
        
        return IfNode(condition, then_body, elifs, else_body)
    
    def _parse_loop_block(self) -> LoopNode:
        """Parse loop block: given expression ":" statement* "done" """
        self._consume('GIVEN', "Expected 'given'")
        
        iterator_var = None
        
        # Handle "i in range(3)" pattern
        if self._check('IDENT') and self._peek_next().type == 'IN':
            # Iterator pattern: given i in range(3):
            iterator_var = self._advance().value  # consume identifier
            self._consume('IN', "Expected 'in'")
            iterable = self._parse_expression()
            condition_or_iter = iterable
            loop_kind = "iterator"
        else:
            # While pattern: given x > 0:
            condition_or_iter = self._parse_expression()
            loop_kind = "while"
        
        self._consume('COLON', "Expected ':' after given expression")
        
        body = []
        while not self._check('DONE') and not self._is_at_end():
            # Skip NEWLINE tokens
            while self._match('NEWLINE'):
                pass
            
            if self._check('DONE'):
                break
                
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
        
        self._consume('DONE', "Expected 'done' after loop body")
        
        return LoopNode(condition_or_iter, loop_kind, body, iterator_var)
    
    def _parse_assignment_or_expr_stmt(self):
        """Parse assignment or expression statement."""
        if self._check('IDENT'):
            # Check if it's an assignment
            if self._peek_next().type == 'ASSIGN':
                # Assignment: IDENT "=" expression
                name_token = self._advance()
                name = name_token.value
                
                self._advance()  # consume '='
                expr = self._parse_expression()
                
                return AssignNode(name, expr)
            elif (self._peek_next().type == 'DOT' and 
                  self._peek_next_next().type == 'IDENT' and 
                  self._peek_next_next_next().type == 'ASSIGN'):
                # Assignment to member: obj.attr = expression
                obj_name = self._advance().value
                self._advance()  # consume '.'
                member_name = self._advance().value
                self._advance()  # consume '='
                
                full_name = f"{obj_name}.{member_name}"
                expr = self._parse_expression()
                
                return AssignNode(full_name, expr)
        
        # Expression statement
        return self._parse_expression()
    
    def _parse_return_stmt(self) -> ReturnNode:
        """Parse return statement: return expression? """
        self._consume('RETURN', "Expected 'return'")
        
        value = None
        if not self._check('NEWLINE') and not self._check('EOF'):
            value = self._parse_expression()
        
        return ReturnNode(value)
    
    def _parse_expression(self):
        """Parse an expression with proper precedence."""
        return self._parse_logical_or()
    
    def _parse_logical_or(self):
        """Parse logical OR expressions."""
        expr = self._parse_logical_and()
        
        while self._match('OR'):
            operator = self._previous().value
            right = self._parse_logical_and()
            expr = BinaryOpNode(operator, expr, right)
        
        return expr
    
    def _parse_logical_and(self):
        """Parse logical AND expressions."""
        expr = self._parse_equality()
        
        while self._match('AND'):
            operator = self._previous().value
            right = self._parse_equality()
            expr = BinaryOpNode(operator, expr, right)
        
        return expr
    
    def _parse_equality(self):
        """Parse equality expressions (==, !=)."""
        expr = self._parse_comparison()
        
        while self._match('==', '!='):
            operator = self._previous().value
            right = self._parse_comparison()
            expr = BinaryOpNode(operator, expr, right)
        
        return expr
    
    def _parse_comparison(self):
        """Parse comparison expressions (<, <=, >, >=)."""
        expr = self._parse_term()
        
        while self._match('LT', '<=', 'GT', '>='):
            operator = self._previous().value
            right = self._parse_term()
            expr = BinaryOpNode(operator, expr, right)
        
        return expr
    
    def _parse_term(self):
        """Parse addition and subtraction."""
        expr = self._parse_factor()
        
        while self._match('PLUS', 'MINUS'):
            operator = self._previous().value
            right = self._parse_factor()
            expr = BinaryOpNode(operator, expr, right)
        
        return expr
    
    def _parse_factor(self):
        """Parse multiplication and division."""
        expr = self._parse_unary()
        
        while self._match('MULTIPLY', 'DIVIDE'):
            operator = self._previous().value
            right = self._parse_unary()
            expr = BinaryOpNode(operator, expr, right)
        
        return expr
    
    def _parse_unary(self):
        """Parse unary expressions (-, !)."""
        if self._match('MINUS', 'NOT'):
            operator = self._previous().value
            right = self._parse_unary()
            return UnaryOpNode(operator, right)
        
        return self._parse_primary()
    
    def _parse_primary(self):
        """Parse primary expressions."""
        if self._match('INT', 'FLOAT'):
            return LiteralNode(self._previous().value)
        
        if self._match('STRING'):
            return LiteralNode(self._previous().value)
        
        if self._match('IDENT'):
            name = self._previous().value
            
            # Check if it's a function call
            if self._match('LPAREN'):
                args = []
                if not self._check('RPAREN'):
                    args = self._parse_argument_list()
                
                self._consume('RPAREN', "Expected ')' after arguments")
                return CallNode(name, args)
            
            # Handle member access: obj.member
            if self._match('DOT'):
                member_name = self._consume('IDENT', "Expected member name after '.'").value
                full_name = f"{name}.{member_name}"
                
                # Check if it's a method call: obj.method()
                if self._match('LPAREN'):
                    args = []
                    if not self._check('RPAREN'):
                        args = self._parse_argument_list()
                    
                    self._consume('RPAREN', "Expected ')' after arguments")
                    return CallNode(full_name, args)
                
                return IdentifierNode(full_name)
            
            return IdentifierNode(name)
        
        if self._match('LPAREN'):
            expr = self._parse_expression()
            self._consume('RPAREN', "Expected ')' after expression")
            return expr
        
        if self._match('LBRACKET'):
            # List literal: [ expression* ]
            elements = []
            if not self._check('RBRACKET'):
                elements.append(self._parse_expression())
                while self._match('COMMA'):
                    elements.append(self._parse_expression())
            self._consume('RBRACKET', "Expected ']' after list elements")
            return ListLiteralNode(elements)
        
        raise SyntaxErrorLyric("Expected expression", self._peek().line, self._peek().col)
    
    def _parse_argument_list(self) -> List:
        """Parse argument list: expression ("," expression)*"""
        args = []
        
        args.append(self._parse_expression())
        
        while self._match('COMMA'):
            args.append(self._parse_expression())
        
        return args
    
    def _previous(self) -> Token:
        """Get the previous token."""
        return self.tokens[self.current - 1]
    
    def _peek_next(self) -> Token:
        """Look at the next token without advancing."""
        if self.current + 1 >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[self.current + 1]
    
    def _peek_next_next(self) -> Token:
        """Look at the token after next without advancing."""
        if self.current + 2 >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[self.current + 2]
    
    def _peek_next_next_next(self) -> Token:
        """Look at the token after next next without advancing."""
        if self.current + 3 >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[self.current + 3]


def parse(source: str) -> ProgramNode:
    """Parse source code and return a ProgramNode."""
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse()