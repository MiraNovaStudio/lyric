"""Parser module for converting tokens to AST."""

from typing import List
from lyric.lexer import Token, tokenize
from lyric.ast_nodes import (
    ProgramNode, FunctionNode, IfNode, LoopNode, AssignNode, CallNode,
    BinaryOpNode, UnaryOpNode, LiteralNode, IdentifierNode, ClassNode, ReturnNode, 
    ListLiteralNode, DictLiteralNode, IndexNode, TypeDeclarationNode, MultiDeclarationNode, TryNode, RaiseNode, ImportPyNode
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
        """Parse function definition: def IDENT "(" param_list? ")" "{" statement* "}" """
        def_token = self._consume('DEF', "Expected 'def'")
        
        name_token = self._consume('IDENT', "Expected function name")
        name = name_token.value
        
        self._consume('LPAREN', "Expected '(' after function name")
        
        params = []
        param_types = []
        if not self._check('RPAREN'):
            params, param_types = self._parse_param_list()
        
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
        
        return FunctionNode(name, params, param_types, body_statements, def_token.line, def_token.col)
    
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
        if self._check('IDENT', 'TYPE_OR_IDENT'):
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
            elif (self._peek_next().type == 'LBRACKET' and 
                  self._peek_next_next().type in ('STRING', 'INT', 'FLOAT', 'IDENT') and
                  self._peek_next_next_next().type == 'RBRACKET' and
                  self._peek_next_next_next_next().type == 'ASSIGN'):
                # Assignment to indexed expression: obj[index] = expression
                obj_name = self._advance().value
                self._advance()  # consume '['
                index_token = self._advance()
                self._advance()  # consume ']'
                self._advance()  # consume '='
                
                # Create the indexed assignment
                index_expr = LiteralNode(index_token.value)
                indexed_expr = IndexNode(IdentifierNode(obj_name), index_expr)
                expr = self._parse_expression()
                
                return AssignNode(f"{obj_name}[{index_token.value}]", expr)
        
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
        
        if self._match('BOOLEAN'):
            return LiteralNode(self._previous().value)
        
        if self._match('NONE'):
            return LiteralNode(None)
        
        if self._match('IDENT', 'TYPE_OR_IDENT'):
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
                    return CallNode(full_name, args)
                
                return IdentifierNode(full_name)
            
            # Start with identifier and check for indexing
            expr = IdentifierNode(name)
            return self._parse_indexing_chain(expr)
        
        if self._match('LPAREN'):
            expr = self._parse_expression()
            self._consume('RPAREN', "Expected ')' after expression")
            return self._parse_indexing_chain(expr)
        
        if self._match('LBRACKET'):
            # List literal: [ expression* ]
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
            return self._parse_indexing_chain(ListLiteralNode(elements))
        
        if self._match('LBRACE'):
            # Dictionary literal: { key: value, ... }
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
            return self._parse_indexing_chain(DictLiteralNode(pairs))
        
        raise SyntaxErrorLyric("Expected expression", self._peek().line, self._peek().col)
    
    def _parse_indexing_chain(self, expr):
        """Parse chained indexing operations: expr[index][index]..."""
        while self._match('LBRACKET'):
            index = self._parse_expression()
            self._consume('RBRACKET', "Expected ']' after index")
            expr = IndexNode(expr, index)
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
        """Parse try/catch/finally block: try: ... catch: ... finally: ... fade"""
        self._consume('TRY', "Expected 'try'")
        self._consume('COLON', "Expected ':' after try")
        
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
        
        # Parse catch block (optional)
        catch_body = None
        if self._match('CATCH'):
            self._consume('COLON', "Expected ':' after catch")
            
            catch_body = []
            while not self._check('FINALLY', 'FADE') and not self._is_at_end():
                # Skip NEWLINE tokens
                while self._match('NEWLINE'):
                    pass
                
                if self._check('FINALLY', 'FADE'):
                    break
                    
                stmt = self._parse_statement()
                if stmt:
                    catch_body.append(stmt)
        
        # Parse finally block (optional)
        finally_body = None
        if self._match('FINALLY'):
            self._consume('COLON', "Expected ':' after finally")
            
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
        if catch_body is None:
            raise ParseError("try block must have a catch block at line {}, column {}".format(
                self._peek().line, self._peek().col))
        
        return TryNode(try_body, catch_body, finally_body)

    def _parse_raise_stmt(self) -> RaiseNode:
        """Parse raise statement: raise ExceptionName"""
        self._consume('RAISE', "Expected 'raise'")
        
        # Parse exception name
        exception_token = self._consume('IDENT', "Expected exception name after 'raise'")
        exception_name = exception_token.value
        
        return RaiseNode(exception_name)

    def _parse_type_declaration(self) -> TypeDeclarationNode:
        """Parse type declaration: TYPE IDENT "=" expression"""
        type_token = self._advance()
        type_name = type_token.value.lower()
        
        # Validate that pyobject is not allowed as explicit type declaration
        if type_name == 'pyobject':
            raise ParseError(f"Type 'pyobject' is internal only and cannot be used in explicit declarations at line {type_token.line}, column {type_token.col}")
        
        # Validate that the type is a known type
        valid_types = {'int', 'str', 'flt', 'var'}
        if type_name not in valid_types:
            raise ParseError(f"Unknown type '{type_name}' at line {type_token.line}, column {type_token.col}. Valid types are: {', '.join(valid_types)}")
        
        name_token = self._consume('IDENT', "Expected variable name after type")
        name = name_token.value
        
        self._consume('ASSIGN', "Expected '=' after variable name")
        expr = self._parse_expression()
        
        return TypeDeclarationNode(type_name, name, expr)
    
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
            valid_types = {'int', 'str', 'flt', 'var'}
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