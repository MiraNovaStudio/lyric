# Lyric Programming Language
# Copyright (c) 2025 MiraNova Studios
# Designed and Architected by Michael (Aeonath) and ChatGPT
# Implemented by Claude
# Licensed under the MIT License with Source Attribution

"""Parser module for converting tokens to AST."""

from typing import List
from lyric.lexer import Token, tokenize
from lyric.ast_nodes import (
    ProgramNode, FunctionNode, IfNode, LoopNode, AssignNode, CallNode,
    BinaryOpNode, UnaryOpNode, LiteralNode, IdentifierNode, ClassNode, ReturnNode, BreakNode, ContinueNode,
    ListLiteralNode, DictLiteralNode, IndexNode, SliceNode, TypeDeclarationNode, MultiDeclarationNode, TryNode, CatchClauseNode, RaiseNode, ImportPyNode
)
from lyric.errors import ParseError, SyntaxErrorLyric


class Parser:
    """Recursive descent parser for Lyric language."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.loop_depth = 0  # Track nesting level for break/continue validation
    
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
        
        if self._check('TYPE_OR_IDENT') and self._peek_next().type == 'DEF':
            return self._parse_func_def()
        elif self._check('DEF'):
            return self._parse_func_def()
        elif self._check('CLASS'):
            return self._parse_class_def()
        elif self._check('IF'):
            return self._parse_if_block()
        elif self._check('GIVEN'):
            return self._parse_loop_block()
        elif self._check('RETURN'):
            return self._parse_return_stmt()
        elif self._check('BREAK'):
            return self._parse_break_stmt()
        elif self._check('CONTINUE'):
            return self._parse_continue_stmt()
        elif self._check('TRY'):
            return self._parse_try_block()
        elif self._check('IMPORTPY'):
            return self._parse_importpy_stmt()
        elif self._check('RAISE'):
            return self._parse_raise_stmt()
        elif self._check('TYPE_OR_IDENT') and self._peek_next().type == 'IDENT' and self._peek_next_next().type == 'COMMA':
            return self._parse_multi_declaration()
        elif self._check('TYPE_OR_IDENT') and self._peek_next().type == 'IDENT' and self._peek_next_next().type == 'ASSIGN':
            return self._parse_type_declaration()
        elif self._check('TYPE_OR_IDENT') and self._peek_next().type == 'IDENT':
            # Single variable declaration without assignment
            return self._parse_multi_declaration()
        elif self._check('IDENT') and self._peek_next().type == 'IDENT' and self._peek_next_next().type == 'COMMA':
            # Multi-declaration with invalid type - let multi-declaration parser handle the error
            return self._parse_multi_declaration()
        elif self._check('TYPE_OR_IDENT') and self._peek_next().type == 'ASSIGN':
            # Error: type keyword followed directly by assignment (missing variable name)
            type_token = self._advance()
            self._advance()  # consume '='
            raise ParseError(f"Expected variable name after type '{type_token.value}' at line {type_token.line}, column {type_token.col}")
        else:
            return self._parse_assignment_or_expr_stmt()
    
    def _parse_func_def(self) -> FunctionNode:
        """Parse function definition: [TYPE] def IDENT "(" param_list? ")" [":"] "{" statement* "}" """
        return_type = None
        
        # Check for optional return type before 'def'
        if self._check('TYPE_OR_IDENT') and self._peek_next().type == 'DEF':
            type_token = self._advance()
            return_type = type_token.value.lower()
        
        def_token = self._consume('DEF', "Expected 'def'")
        
        name_token = self._consume('IDENT', "Expected function name")
        name = name_token.value
        
        self._consume('LPAREN', "Expected '(' after function name")
        
        params = []
        param_types = []
        if not self._check('RPAREN'):
            params, param_types = self._parse_param_list()
        
        self._consume('RPAREN', "Expected ')' after parameters")
        
        # Make colon optional after function signature
        self._match('COLON')  # Optional colon
        
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
        
        return FunctionNode(name, params, param_types, return_type, body_statements, def_token.line, def_token.col)
    
    def _parse_param_list(self) -> tuple[List[str], List[str]]:
        """Parse parameter list: (TYPE IDENT | IDENT) ("," (TYPE IDENT | IDENT))*"""
        params = []
        param_types = []
        
        # Parse first parameter
        if self._check('TYPE_OR_IDENT', 'IDENT'):
            if self._check('TYPE_OR_IDENT') and self._peek_next().type == 'IDENT':
                # Typed parameter: TYPE IDENT
                type_token = self._advance()
                param_token = self._advance()
                param_types.append(type_token.value.lower())
                params.append(param_token.value)
            elif self._check('TYPE_OR_IDENT') and self._peek_next().type == 'RPAREN':
                # Error: TYPE without parameter name
                type_token = self._advance()
                raise ParseError(
                    f"Expected parameter name after type '{type_token.value}' at line {type_token.line}, "
                    f"column {type_token.col}")
            else:
                # Untyped parameter: IDENT
                param_token = self._advance()
                param_types.append('var')  # Default to var type
                params.append(param_token.value)
            
            # Parse remaining parameters
            while self._match('COMMA'):
                if self._check('TYPE_OR_IDENT') and self._peek_next().type == 'IDENT':
                    # Typed parameter: TYPE IDENT
                    type_token = self._advance()
                    param_token = self._advance()
                    param_types.append(type_token.value.lower())
                    params.append(param_token.value)
                elif self._check('TYPE_OR_IDENT') and self._peek_next().type in ('RPAREN', 'COMMA'):
                    # Error: TYPE without parameter name
                    type_token = self._advance()
                    raise ParseError(
                        f"Expected parameter name after type '{type_token.value}' at line {type_token.line}, "
                        f"column {type_token.col}")
                elif self._check('IDENT'):
                    # Untyped parameter: IDENT
                    param_token = self._advance()
                    param_types.append('var')  # Default to var type
                    params.append(param_token.value)
                else:
                    raise ParseError(
                        f"Expected parameter name after ',' at line {self._peek().line}, "
                        f"column {self._peek().col}")
        
        return params, param_types
    
    def _parse_class_def(self) -> ClassNode:
        """Parse class definition: class IDENT [":"] statement* CLASS_END"""
        class_token = self._consume('CLASS', "Expected 'class'")
        
        name_token = self._consume('IDENT', "Expected class name")
        name = name_token.value
        
        # Make colon optional after class name
        self._match('COLON')  # Optional colon
        
        members_statements = []
        constructor_method = None
        
        while not self._check('CLASS_END') and not self._is_at_end():
            # Skip NEWLINE tokens
            while self._match('NEWLINE'):
                pass
            
            if self._check('CLASS_END'):
                break
                
            stmt = self._parse_statement()
            if stmt:
                # Check if this is a constructor method (method name matches class name)
                if isinstance(stmt, FunctionNode) and stmt.name == name:
                    if constructor_method is not None:
                        # Multiple constructors found - this is an error
                        raise ParseError(
                            f"Multiple constructors found for class '{name}'. Only one constructor method is allowed per class. "
                            f"Found constructor at line {constructor_method.line}, column {constructor_method.column} "
                            f"and another at line {stmt.line}, column {stmt.column}",
                            stmt.line, stmt.column
                        )
                    constructor_method = stmt
                else:
                    members_statements.append(stmt)
        
        self._consume('CLASS_END', "Expected '+++' after class body")
        
        return ClassNode(name, members_statements, constructor_method, class_token.line, class_token.col)
    
    def _parse_if_block(self) -> IfNode:
        """Parse if block: if expression [":"] statement* ("else" "if" expression [":"] statement*)* ("else" [":"] statement*)? "end" """
        if_token = self._consume('IF', "Expected 'if'")
        
        condition = self._parse_expression()
        
        # Make colon optional after if condition
        self._match('COLON')  # Optional colon
        
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
                
                # Make colon optional after elif condition
                self._match('COLON')  # Optional colon
                
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
                # Make colon optional after else
                self._match('COLON')  # Optional colon
                
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
        
        return IfNode(condition, then_body, elifs, else_body, if_token.line, if_token.col)
    
    def _parse_loop_block(self) -> LoopNode:
        """Parse loop block: given expression [":"] statement* "done" """
        given_token = self._consume('GIVEN', "Expected 'given'")
        
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
        
        # Make colon optional after given expression
        self._match('COLON')  # Optional colon
        
        # Increment loop depth for break/continue validation
        self.loop_depth += 1
        
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
        
        # Decrement loop depth
        self.loop_depth -= 1
        
        self._consume('DONE', "Expected 'done' after loop body")
        
        return LoopNode(condition_or_iter, loop_kind, body, iterator_var, given_token.line, given_token.col)
    
    def _parse_assignment_or_expr_stmt(self):
        """Parse assignment or expression statement."""
        if self._check('IDENT', 'TYPE_OR_IDENT'):
            # Check for print statement syntax: print <expr>
            if (self._peek().value == 'print' and 
                self._peek_next().type != 'LPAREN' and 
                not self._check('NEWLINE') and 
                not self._check('EOF')):
                # Parse print <expr> syntax (single or multiple arguments)
                print_token = self._advance()
                args = []
                
                # Parse first expression
                expr = self._parse_expression()
                args.append(expr)
                
                # Parse additional expressions separated by commas
                while self._match('COMMA'):
                    expr = self._parse_expression()
                    args.append(expr)
                
                # Create CallNode with arguments to match print(<expr>) AST
                return CallNode('print', args, print_token.line, print_token.col)
            
            # Check if it's an assignment
            elif self._peek_next().type == 'ASSIGN':
                # Assignment: IDENT "=" expression
                name_token = self._advance()
                name = name_token.value
                
                self._advance()  # consume '='
                expr = self._parse_expression()
                
                return AssignNode(name, expr, name_token.line, name_token.col)
            elif (self._peek_next().type == 'DOT' and 
                  self._peek_next_next().type == 'IDENT' and 
                  self._peek_next_next_next().type == 'ASSIGN'):
                # Assignment to member: obj.attr = expression
                obj_token = self._advance()
                obj_name = obj_token.value
                self._advance()  # consume '.'
                member_name = self._advance().value
                self._advance()  # consume '='
                
                full_name = f"{obj_name}.{member_name}"
                expr = self._parse_expression()
                
                return AssignNode(full_name, expr, obj_token.line, obj_token.col)
            elif (self._peek_next().type == 'LBRACKET' and 
                  self._peek_next_next().type in ('STRING', 'INT', 'FLOAT', 'IDENT') and
                  self._peek_next_next_next().type == 'RBRACKET' and
                  self._peek_next_next_next_next().type == 'ASSIGN'):
                # Assignment to indexed expression: obj[index] = expression
                obj_token = self._advance()
                obj_name = obj_token.value
                self._advance()  # consume '['
                index_token = self._advance()
                self._advance()  # consume ']'
                self._advance()  # consume '='
                
                # Create the indexed assignment
                index_expr = LiteralNode(index_token.value)
                indexed_expr = IndexNode(IdentifierNode(obj_name), index_expr)
                expr = self._parse_expression()
                
                return AssignNode(f"{obj_name}[{index_token.value}]", expr, obj_token.line, obj_token.col)
        
        # Expression statement
        return self._parse_expression()
    
    def _parse_return_stmt(self) -> ReturnNode:
        """Parse return statement: return expression? """
        return_token = self._consume('RETURN', "Expected 'return'")
        
        value = None
        if not self._check('NEWLINE') and not self._check('EOF'):
            value = self._parse_expression()
        
        return ReturnNode(value, return_token.line, return_token.col)
    
    def _parse_break_stmt(self) -> BreakNode:
        """Parse break statement: break """
        break_token = self._consume('BREAK', "Expected 'break'")
        
        # Validate that break is used within a loop context
        if self.loop_depth == 0:
            raise ParseError(f"'break' used outside of loop at line {break_token.line}, column {break_token.col}")
        
        return BreakNode(break_token.line, break_token.col)
    
    def _parse_continue_stmt(self) -> ContinueNode:
        """Parse continue statement: continue """
        continue_token = self._consume('CONTINUE', "Expected 'continue'")
        
        # Validate that continue is used within a loop context
        if self.loop_depth == 0:
            raise ParseError(f"'continue' used outside of loop at line {continue_token.line}, column {continue_token.col}")
        
        return ContinueNode(continue_token.line, continue_token.col)
    
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
            line, col = self._get_position_from_token(self._previous())
            expr = BinaryOpNode(operator, expr, right, line, col)
        
        return expr
    
    def _parse_equality(self):
        """Parse equality expressions (==, !=)."""
        expr = self._parse_comparison()
        
        while self._match('==', '!='):
            operator = self._previous().value
            right = self._parse_comparison()
            line, col = self._get_position_from_token(self._previous())
            expr = BinaryOpNode(operator, expr, right, line, col)
        
        return expr
    
    def _parse_comparison(self):
        """Parse comparison expressions (<, <=, >, >=)."""
        expr = self._parse_term()
        
        while self._match('LT', '<=', 'GT', '>='):
            operator = self._previous().value
            right = self._parse_term()
            line, col = self._get_position_from_token(self._previous())
            expr = BinaryOpNode(operator, expr, right, line, col)
        
        return expr
    
    def _parse_term(self):
        """Parse addition and subtraction."""
        expr = self._parse_factor()
        
        while self._match('PLUS', 'MINUS'):
            operator = self._previous().value
            right = self._parse_factor()
            line, col = self._get_position_from_token(self._previous())
            expr = BinaryOpNode(operator, expr, right, line, col)
        
        return expr
    
    def _parse_factor(self):
        """Parse multiplication and division."""
        expr = self._parse_unary()
        
        while self._match('MULTIPLY', 'DIVIDE'):
            operator = self._previous().value
            right = self._parse_unary()
            line, col = self._get_position_from_token(self._previous())
            expr = BinaryOpNode(operator, expr, right, line, col)
        
        return expr
    
    def _parse_unary(self):
        """Parse unary expressions (-, !)."""
        if self._match('MINUS', 'NOT'):
            operator = self._previous().value
            right = self._parse_unary()
            line, col = self._get_position_from_token(self._previous())
            return UnaryOpNode(operator, right, line, col)
        
        return self._parse_primary()
    
    def _parse_primary(self):
        """Parse primary expressions."""
        if self._match('INT', 'FLOAT'):
            token = self._previous()
            return LiteralNode(token.value, token.line, token.col)
        
        if self._match('STRING'):
            token = self._previous()
            return LiteralNode(token.value, token.line, token.col)
        
        if self._match('BOOLEAN'):
            token = self._previous()
            return LiteralNode(token.value, token.line, token.col)
        
        if self._match('NONE'):
            token = self._previous()
            return LiteralNode(None, token.line, token.col)
        
        if self._match('IDENT', 'TYPE_OR_IDENT'):
            name_token = self._previous()
            name = name_token.value
            
            # Check if it's a function call
            if self._match('LPAREN'):
                args = []
                if not self._check('RPAREN'):
                    args = self._parse_argument_list()
                
                self._consume('RPAREN', "Expected ')' after arguments")
                return CallNode(name, args, name_token.line, name_token.col)
            
            # Handle member access: obj.member
            if self._match('DOT'):
                member_name = self._consume('IDENT', "Expected member name after '.'").value
                full_name = f"{name}.{member_name}"
                
                # Handle chained member access: obj.member.member
                while self._match('DOT'):
                    next_member = self._consume('IDENT', "Expected member name after '.'").value
                    full_name = f"{full_name}.{next_member}"
                
                # Check if it's a method call: obj.method()
                if self._match('LPAREN'):
                    args = []
                    if not self._check('RPAREN'):
                        args = self._parse_argument_list()
                    
                    self._consume('RPAREN', "Expected ')' after arguments")
                    return CallNode(full_name, args, name_token.line, name_token.col)
                
                return IdentifierNode(full_name, name_token.line, name_token.col)
            
            # Start with identifier and check for indexing
            expr = IdentifierNode(name, name_token.line, name_token.col)
            return self._parse_indexing_chain(expr)
        
        if self._match('LPAREN'):
            lparen_token = self._previous()
            expr = self._parse_expression()
            self._consume('RPAREN', "Expected ')' after expression")
            # Use the position of the opening parenthesis
            expr.line, expr.column = lparen_token.line, lparen_token.col
            return self._parse_indexing_chain(expr)
        
        if self._match('LBRACKET'):
            # List literal: [ expression* ]
            lbracket_token = self._previous()
            elements = []
            if not self._check('RBRACKET'):
                # Skip NEWLINE tokens
                while self._match('NEWLINE'):
                    pass
                
                elements.append(self._parse_expression())
                while self._match('COMMA'):
                    # Skip NEWLINE tokens
                    while self._match('NEWLINE'):
                        pass
                    elements.append(self._parse_expression())
            
            # Skip NEWLINE tokens before closing bracket
            while self._match('NEWLINE'):
                pass
            
            self._consume('RBRACKET', "Expected ']' after list elements")
            return self._parse_indexing_chain(ListLiteralNode(elements, lbracket_token.line, lbracket_token.col))
        
        if self._match('LBRACE'):
            # Dictionary literal: { key: value, ... }
            lbrace_token = self._previous()
            pairs = []
            if not self._check('RBRACE'):
                # Skip NEWLINE tokens
                while self._match('NEWLINE'):
                    pass
                
                # Parse first key-value pair
                key = self._parse_expression()
                self._consume('COLON', "Expected ':' after dictionary key")
                value = self._parse_expression()
                pairs.append((key, value))
                
                # Parse remaining pairs
                while self._match('COMMA'):
                    # Skip NEWLINE tokens
                    while self._match('NEWLINE'):
                        pass
                    key = self._parse_expression()
                    self._consume('COLON', "Expected ':' after dictionary key")
                    value = self._parse_expression()
                    pairs.append((key, value))
            
            # Skip NEWLINE tokens before closing brace
            while self._match('NEWLINE'):
                pass
            
            self._consume('RBRACE', "Expected '}' after dictionary pairs")
            return self._parse_indexing_chain(DictLiteralNode(pairs, lbrace_token.line, lbrace_token.col))
        
        raise SyntaxErrorLyric("Expected expression", self._peek().line, self._peek().col)
    
    def _parse_indexing_chain(self, expr):
        """Parse chained indexing operations: expr[index][index]... or expr[start:end:step]..."""
        while self._match('LBRACKET'):
            lbracket_token = self._previous()
            
            # Check if this is slicing syntax (contains colons)
            # Look ahead to see if there's a colon in the bracket
            is_slice = False
            temp_pos = self.current
            while temp_pos < len(self.tokens) and self.tokens[temp_pos].type != 'RBRACKET':
                if self.tokens[temp_pos].type == 'COLON':
                    is_slice = True
                    break
                temp_pos += 1
            
            if is_slice:
                # Parse slice: [start:end:step]
                start = None
                end = None
                step = None
                
                # Parse start (if present)
                if not self._check('COLON'):
                    start = self._parse_expression()
                
                # Parse first colon
                if self._match('COLON'):
                    # Parse end (if present)
                    if not self._check('COLON', 'RBRACKET'):
                        end = self._parse_expression()
                    
                    # Parse second colon and step (if present)
                    if self._match('COLON'):
                        if not self._check('RBRACKET'):
                            step = self._parse_expression()
                
                self._consume('RBRACKET', "Expected ']' after slice")
                expr = SliceNode(expr, start, end, step, lbracket_token.line, lbracket_token.col)
            else:
                # Parse simple index: [index]
                index = self._parse_expression()
                self._consume('RBRACKET', "Expected ']' after index")
                expr = IndexNode(expr, index, lbracket_token.line, lbracket_token.col)
        
        return expr
    
    def _parse_argument_list(self) -> List:
        """Parse argument list: expression ("," expression)*"""
        args = []
        
        args.append(self._parse_expression())
        
        while self._match('COMMA'):
            args.append(self._parse_expression())
        
        return args
    
    def _parse_type_declaration(self) -> TypeDeclarationNode:
        """Parse type declaration: TYPE IDENT "=" expression"""
        type_token = self._advance()  # Consume the type token (INT, STR, FLT, VAR)
        type_name = type_token.value.lower()  # Convert to lowercase (int, str, flt, var)
        
        name_token = self._consume('IDENT', "Expected variable name after type")
        name = name_token.value
        
        self._consume('ASSIGN', "Expected '=' after variable name")
        
        expr = self._parse_expression()
        
        return TypeDeclarationNode(type_name, name, expr)
    
    def _previous(self) -> Token:
        """Get the previous token."""
        return self.tokens[self.current - 1]
    
    def _get_position_from_token(self, token: Token) -> tuple[int, int]:
        """Get line and column position from a token."""
        return (token.line, token.col)
    
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
    
    def _peek_next_next_next_next(self) -> Token:
        """Look at the token 4 positions ahead without advancing."""
        if self.current + 4 >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[self.current + 4]

    def _parse_try_block(self) -> TryNode:
        """Parse try/catch/finally block: try [":"] ... catch [Type] [as var] [":"] ... finally [":"] ... fade"""
        try_token = self._consume('TRY', "Expected 'try'")
        
        # Make colon optional after try
        self._match('COLON')  # Optional colon
        
        # Parse try body
        try_body = []
        while not self._check('CATCH', 'FINALLY', 'FADE') and not self._is_at_end():
            # Skip NEWLINE tokens
            while self._match('NEWLINE'):
                pass
            
            if self._check('CATCH', 'FINALLY', 'FADE'):
                break
                
            stmt = self._parse_statement()
            if stmt:
                try_body.append(stmt)
        
        # Parse catch clauses (multiple allowed)
        catch_clauses = []
        while self._match('CATCH'):
            catch_clause = self._parse_catch_clause()
            catch_clauses.append(catch_clause)
        
        # Parse finally block (optional)
        finally_body = None
        if self._match('FINALLY'):
            # Make colon optional after finally
            self._match('COLON')  # Optional colon
            
            finally_body = []
            while not self._check('FADE') and not self._is_at_end():
                # Skip NEWLINE tokens
                while self._match('NEWLINE'):
                    pass
                
                if self._check('FADE'):
                    break
                    
                stmt = self._parse_statement()
                if stmt:
                    finally_body.append(stmt)
        
        # Consume fade
        self._consume('FADE', "Expected 'fade' to end try block")
        
        # Validate: try without catch is a syntax error
        if not catch_clauses:
            raise ParseError("try block must have at least one catch block at line {}, column {}".format(
                self._peek().line, self._peek().col))
        
        return TryNode(try_body, catch_clauses, finally_body, try_token.line, try_token.col)
    
    def _parse_catch_clause(self) -> CatchClauseNode:
        """Parse a single catch clause: catch [Type] [as identifier] [":"] ... """
        exception_type = None
        variable_name = None
        
        # Check for exception type (IDENT after CATCH)
        if self._check('IDENT'):
            exception_type = self._advance().value
        
        # Check for 'as' keyword
        if self._match('AS'):
            if self._check('IDENT'):
                variable_name = self._advance().value
            else:
                raise ParseError("Expected variable name after 'as' at line {}, column {}".format(
                    self._peek().line, self._peek().col))
        
        # Make colon optional after catch
        self._match('COLON')  # Optional colon
        
        # Parse catch body
        catch_body = []
        while not self._check('CATCH', 'FINALLY', 'FADE') and not self._is_at_end():
            # Skip NEWLINE tokens
            while self._match('NEWLINE'):
                pass
            
            if self._check('CATCH', 'FINALLY', 'FADE'):
                break
                
            stmt = self._parse_statement()
            if stmt:
                catch_body.append(stmt)
        
        return CatchClauseNode(exception_type, variable_name, catch_body, self._peek().line, self._peek().col)

    def _parse_raise_stmt(self) -> RaiseNode:
        """Parse raise statement: raise ExceptionName"""
        raise_token = self._consume('RAISE', "Expected 'raise'")
        
        # Parse exception name
        exception_token = self._consume('IDENT', "Expected exception name after 'raise'")
        exception_name = exception_token.value
        
        return RaiseNode(exception_name, raise_token.line, raise_token.col)

    def _parse_type_declaration(self) -> TypeDeclarationNode:
        """Parse type declaration: TYPE IDENT "=" expression"""
        type_token = self._advance()
        type_name = type_token.value.lower()
        
        # Validate that pyobject is not allowed as explicit type declaration
        if type_name == 'pyobject':
            raise ParseError(f"Type 'pyobject' is internal only and cannot be used in explicit declarations at line {type_token.line}, column {type_token.col}")
        
        # Validate that the type is a known type
        valid_types = {'int', 'str', 'flt', 'var', 'rex', 'god', 'bin'}
        if type_name not in valid_types:
            raise ParseError(f"Unknown type '{type_name}' at line {type_token.line}, column {type_token.col}. Valid types are: {', '.join(valid_types)}")
        
        name_token = self._consume('IDENT', "Expected variable name after type")
        name = name_token.value
        
        self._consume('ASSIGN', "Expected '=' after variable name")
        expr = self._parse_expression()
        
        return TypeDeclarationNode(type_name, name, expr, type_token.line, type_token.col)
    
    def _parse_multi_declaration(self) -> MultiDeclarationNode:
        """Parse multi-variable declaration: TYPE IDENT "," TYPE IDENT "," ... """
        declarations = []
        line = self._peek().line
        column = self._peek().col
        
        while True:
            # Parse type and variable name
            # Handle both TYPE_OR_IDENT and IDENT (for invalid types)
            if self._check('TYPE_OR_IDENT'):
                type_token = self._consume('TYPE_OR_IDENT', "Expected type keyword")
            else:
                type_token = self._consume('IDENT', "Expected type keyword")
            
            type_name = type_token.value.lower()
            
            # Validate that pyobject is not allowed as explicit type declaration
            if type_name == 'pyobject':
                raise ParseError(f"Type 'pyobject' is internal only and cannot be used in explicit declarations at line {type_token.line}, column {type_token.col}")
            
            # Validate that the type is a known type
            valid_types = {'int', 'str', 'flt', 'var', 'god', 'bin'}
            if type_name not in valid_types:
                raise ParseError(f"Unknown type '{type_name}' at line {type_token.line}, column {type_token.col}. Valid types are: {', '.join(valid_types)}")
            
            name_token = self._consume('IDENT', "Expected variable name after type")
            name = name_token.value
            
            declarations.append((type_name, name))
            
            # Check if there's another declaration
            if self._match('COMMA'):
                continue
            else:
                break
        
        return MultiDeclarationNode(declarations, line, column)
    
    def _parse_importpy_stmt(self) -> ImportPyNode:
        """Parse importpy statement: importpy IDENT"""
        importpy_token = self._consume('IMPORTPY', "Expected 'importpy'")
        module_token = self._consume('IDENT', "Expected module name after 'importpy'")
        
        return ImportPyNode(module_token.value, importpy_token.line, importpy_token.col)


def parse(source: str) -> ProgramNode:
    """Parse source code and return a ProgramNode."""
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse()