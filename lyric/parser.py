"""
Parser module for the Lyric language.
Parses tokens into an Abstract Syntax Tree (AST).
"""

from typing import List, Optional, Union, Dict, Any
from lyric.lexer import Token
from lyric.ast import (
    ProgramNode, FunctionNode, ClassNode, IfNode, ElifNode, LoopNode,
    AssignNode, CallNode, BinaryOpNode, UnaryOpNode, LiteralNode,
    IdentifierNode, ReturnNode, MemberAccessNode, MethodCallNode, IndexNode
)
from lyric.errors import ParseError


class Parser:
    """Recursive descent parser for the Lyric language."""

    def __init__(self, tokens: List[Token], filename: str = None):
        self.tokens = tokens
        self.pos = 0
        self.filename = filename

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
            raise ParseError(f"{message} at end of file", filename=self.filename)
        else:
            raise ParseError(f"{message}", line=current.line, col=current.col,
                             filename=self.filename)

    def _skip_newlines(self):
        """Skip newline tokens."""
        while self._match('NEWLINE'):
            self._advance()

    def _peek_next(self) -> Optional[object]:
        """Peek at the next token without advancing."""
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None

    def _peek_next_next(self) -> Optional[object]:
        """Peek at the token after next without advancing."""
        if self.pos + 2 < len(self.tokens):
            return self.tokens[self.pos + 2]
        return None

    def _peek_next_next_next(self) -> Optional[object]:
        """Peek at the token after next next without advancing."""
        if self.pos + 3 < len(self.tokens):
            return self.tokens[self.pos + 3]
        return None

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
        elif token.type == 'VAR':
            # var keyword for dynamic typing
            return self._parse_assignment_or_expr_stmt()
        elif token.type == 'IDENTIFIER' or token.type == 'NONE' or token.type == 'GOD' or token.type == 'REX':
            # Could be assignment or expression statement
            return self._parse_assignment_or_expr_stmt()
        else:
            # This should not happen in well-formed code
            current = self._peek()
            raise ParseError(f"Unexpected token '{current.value}'",
                             line=current.line, col=current.col, filename=self.filename)

    def _parse_function_def(self) -> FunctionNode:
        """Parse a function definition with C-style type declarations."""
        def_token = self._consume('DEF', "Expected 'def'")
        func_line = def_token.line
        func_col = def_token.col

        # Check for optional return type declaration (C-style: def int func(...) or def rex func(...))
        return_type = None
        if ((self._match('IDENTIFIER') or self._match('NONE') or self._match('GOD') or self._match('REX')) and 
            self._peek_next() and self._peek_next().type == 'IDENTIFIER'):
            # This looks like a return type followed by function name
            if self._match('IDENTIFIER'):
                return_type_token = self._consume('IDENTIFIER', "Expected return type")
            elif self._match('NONE'):
                return_type_token = self._consume('NONE', "Expected return type")
            elif self._match('GOD'):
                return_type_token = self._consume('GOD', "Expected return type")
            else:  # REX
                return_type_token = self._consume('REX', "Expected return type")
            return_type = return_type_token.value

        name_token = self._consume('IDENTIFIER', "Expected function name")
        name = name_token.value

        self._consume('LPAREN', "Expected '('")

        params = []
        param_types = []
        if not self._match('RPAREN'):
            params, param_types = self._parse_param_list()

        self._consume('RPAREN', "Expected ')'")
        self._consume('LBRACE', "Expected '{'")

        # Parse body statements until closing brace
        body_statements = self._parse_function_body()

        self._consume('RBRACE', "Expected '}'")

        return FunctionNode(name=name, params=params, body_statements=body_statements,
                           param_types=param_types if any(param_types) else None,
                           return_type=return_type,
                           filename=self.filename, line=func_line, col=func_col)

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

    def _parse_multi_declaration(self, base_type: str) -> 'MultiDeclareNode':
        """Parse a multi-variable declaration statement.
        
        Args:
            base_type: The base type for the declaration (e.g., 'var', 'int', 'str')
            
        Returns:
            MultiDeclareNode with all declared variables
        """
        from lyric.ast import MultiDeclareNode
        
        declarations = []
        
        # Parse the first variable
        first_var = self._consume('IDENTIFIER', f"Expected variable name after '{base_type}'")
        declarations.append((first_var.value, base_type))
        
        # Parse additional variables
        while self._match('COMMA'):
            self._advance()  # consume ','
            
            # Check if there's a type annotation for this variable
            # Look ahead to see if the next token is a type identifier followed by another identifier
            if ((self._match('IDENTIFIER') or self._match('GOD') or self._match('REX')) and 
                self._peek_next() and self._peek_next().type == 'IDENTIFIER'):
                # This variable has its own type annotation: type var_name, god var_name, or rex var_name
                if self._match('IDENTIFIER'):
                    var_type = self._consume('IDENTIFIER', "Expected variable type")
                elif self._match('GOD'):
                    var_type = self._consume('GOD', "Expected variable type")
                else:  # REX
                    var_type = self._consume('REX', "Expected variable type")
                var_name = self._consume('IDENTIFIER', "Expected variable name")
                declarations.append((var_name.value, var_type.value))
            elif self._match('NONE'):
                # This variable has None type annotation: None var_name
                var_type = self._consume('NONE', "Expected variable type")
                var_name = self._consume('IDENTIFIER', "Expected variable name")
                declarations.append((var_name.value, var_type.value))
            else:
                # This variable uses the base type
                var_name = self._consume('IDENTIFIER', "Expected variable name")
                declarations.append((var_name.value, base_type))
        
        return MultiDeclareNode(declarations)

    def _parse_assignment_or_expr_stmt(self) -> object:
        """Parse assignment or expression statement."""
        # Check if this is a var keyword for dynamic typing: var x = value or var x, int y, str z
        if self._match('VAR'):
            self._advance()  # consume 'var'
            
            # Check if this is a multi-declaration: var x, int y, str z
            if self._peek_next() and self._peek_next().type == 'COMMA':
                return self._parse_multi_declaration('var')
            else:
                # Single var declaration: var x = value
                var_token = self._consume('IDENTIFIER', "Expected variable name after 'var'")
                self._consume('ASSIGN', "Expected '=' after variable name")
                right_expr = self._parse_expression()
                return AssignNode(name=var_token.value, expr=right_expr, 
                                type_annotation='var')
        
        # Check if this is a C-style type-declared variable declaration: int x = value, None x = value, god x = value, or rex x = value
        if self._match('IDENTIFIER') or self._match('NONE') or self._match('GOD') or self._match('REX'):
            # Peek ahead to see if this is a type declaration followed by variable name
            next_token = self._peek_next()
            if (next_token and next_token.type == 'IDENTIFIER' and 
                self._peek_next_next() and self._peek_next_next().type == 'ASSIGN'):
                # This is a C-style type-declared variable: int x = value, None x = value, god x = value, or rex x = value
                if self._match('IDENTIFIER'):
                    type_token = self._consume('IDENTIFIER', "Expected variable type")
                elif self._match('NONE'):
                    type_token = self._consume('NONE', "Expected variable type")
                elif self._match('GOD'):
                    type_token = self._consume('GOD', "Expected variable type")
                else:  # REX
                    type_token = self._consume('REX', "Expected variable type")
                var_token = self._consume('IDENTIFIER', "Expected variable name")
                self._advance()  # consume '='
                right_expr = self._parse_expression()
                return AssignNode(name=var_token.value, expr=right_expr, 
                                type_annotation=type_token.value)
            elif (next_token and next_token.type == 'IDENTIFIER' and 
                  self._peek_next_next() and self._peek_next_next().type == 'COMMA'):
                # This is a multi-declaration: int x, str y, god z, or rex x, int y, str z
                if self._match('IDENTIFIER'):
                    type_token = self._consume('IDENTIFIER', "Expected variable type")
                elif self._match('NONE'):
                    type_token = self._consume('NONE', "Expected variable type")
                elif self._match('GOD'):
                    type_token = self._consume('GOD', "Expected variable type")
                else:  # REX
                    type_token = self._consume('REX', "Expected variable type")
                return self._parse_multi_declaration(type_token.value)
        
        # Parse the left side as an expression
        left_expr = self._parse_expression()

        # Check if this is an assignment
        if self._match('ASSIGN'):
            self._advance()  # consume '='
            right_expr = self._parse_expression()
            # Handle different types of assignment targets
            if isinstance(left_expr, IdentifierNode):
                # Simple variable assignment: x = value
                return AssignNode(name=left_expr.name, expr=right_expr)
            elif isinstance(left_expr, MemberAccessNode):
                # Member access assignment: self.name = value
                return AssignNode(name=left_expr, expr=right_expr)
            else:
                raise ParseError(f"Invalid assignment target: {left_expr}", filename=self.filename)
        else:
            # This is an expression statement
            return left_expr

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

    def _parse_param_list(self) -> tuple[List[str], List[str]]:
        """Parse parameter list with C-style type declarations.
        
        Format: int a, str b, float c
        Returns:
            tuple of (param_names, param_types)
        """
        params = []
        param_types = []

        while True:
            # Check for optional type declaration before parameter name
            param_type = None
            if ((self._match('IDENTIFIER') or self._match('NONE') or self._match('REX')) and 
                self._peek_next() and self._peek_next().type == 'IDENTIFIER'):
                # This looks like a type followed by parameter name
                if self._match('IDENTIFIER'):
                    type_token = self._consume('IDENTIFIER', "Expected parameter type")
                elif self._match('NONE'):
                    type_token = self._consume('NONE', "Expected parameter type")
                else:  # REX
                    type_token = self._consume('REX', "Expected parameter type")
                param_type = type_token.value
            
            param_token = self._consume('IDENTIFIER', "Expected parameter name")
            param_name = param_token.value
            params.append(param_name)
            param_types.append(param_type)

            if self._match('COMMA'):
                self._advance()
            else:
                break

        return params, param_types

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
        elif self._match('NONE'):
            self._advance()
            return LiteralNode(None)
        elif self._match('INTEGER'):
            token = self._advance()
            return LiteralNode(int(token.value))
        elif self._match('FLOAT'):
            token = self._advance()
            return LiteralNode(float(token.value))
        elif self._match('STRING'):
            token = self._advance()
            # Remove quotes from string and unescape
            string_content = token.value[1:-1]
            unescaped = self._unescape_string(string_content)
            return LiteralNode(unescaped)
        elif self._match('REGEX'):
            token = self._advance()
            # Remove slashes from regex and unescape
            regex_content = token.value[1:-1]
            unescaped = self._unescape_string(regex_content)
            from lyric.ast import RegexLiteralNode
            return RegexLiteralNode(unescaped)
        elif self._match('LBRACKET'):
            # Parse list literal
            return self._parse_list_literal()
        elif self._match('LBRACE'):
            # Parse dictionary literal
            return self._parse_dict_literal()
        elif self._match('IDENTIFIER'):
            token = self._advance()

            # Check if this is a function call
            if self._match('LPAREN'):
                return self._parse_call(token.value)
            else:
                expr = IdentifierNode(token.value)
                # Handle postfix operations (indexing, member access, function calls)
                expr = self._parse_postfix_operations(expr)
                return expr
        elif self._match('LPAREN'):
            self._advance()  # consume '('
            expr = self._parse_expression()
            self._consume('RPAREN', "Expected ')' after expression")
            
            # Handle postfix operations after parentheses
            expr = self._parse_postfix_operations(expr)
            
            return expr
        else:
            current = self._peek()
            raise ParseError(f"Unexpected token '{current.value}' at line {current.line}, "
                             f"col {current.col}")

    def _parse_call(self, func_name: str) -> CallNode:
        """Parse a function call."""
        self._consume('LPAREN', "Expected '('")

        args = []
        if not self._match('RPAREN'):
            args = self._parse_arg_list()

        self._consume('RPAREN', "Expected ')'")

        return CallNode(func_name=func_name, args=args)

    def _parse_call_on_expression(self, expr: object) -> Union[CallNode, MethodCallNode]:
        """Parse a function call on an expression (for method calls)."""
        self._consume('LPAREN', "Expected '('")

        args = []
        if not self._match('RPAREN'):
            args = self._parse_arg_list()

        self._consume('RPAREN', "Expected ')'")

        # Create appropriate node based on expression type
        if isinstance(expr, MemberAccessNode):
            return MethodCallNode(object=expr.object, method=expr.member, args=args)
        elif isinstance(expr, IdentifierNode):
            return CallNode(func_name=expr.name, args=args)
        else:
            raise ParseError(f"Cannot call expression of type {type(expr)}")

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

    def _parse_list_literal(self) -> LiteralNode:
        """Parse a list literal [item1, item2, ...]."""
        self._consume('LBRACKET', "Expected '['")
        
        element_nodes = []
        if not self._match('RBRACKET'):
            element_nodes = self._parse_list_elements()
        
        self._consume('RBRACKET', "Expected ']'")
        
        # For now, we'll keep the AST nodes and evaluate them at runtime
        # This allows for more complex expressions in list literals
        return LiteralNode(element_nodes)

    def _parse_list_elements(self) -> List[object]:
        """Parse list elements separated by commas."""
        elements = []
        
        while True:
            element = self._parse_expression()
            elements.append(element)
            
            if self._match('COMMA'):
                self._advance()
            else:
                break
        
        return elements

    def _parse_dict_literal(self) -> LiteralNode:
        """Parse a dictionary literal {key1: value1, key2: value2, ...}."""
        self._consume('LBRACE', "Expected '{'")
        
        pairs = {}
        if not self._match('RBRACE'):
            pairs = self._parse_dict_pairs()
        
        self._consume('RBRACE', "Expected '}'")
        return LiteralNode(pairs)

    def _parse_dict_pairs(self) -> Dict[Any, Any]:
        """Parse dictionary key-value pairs separated by commas."""
        pairs = {}
        
        while True:
            # Parse key
            key = self._parse_expression()
            
            # Parse colon
            self._consume('COLON', "Expected ':' after dictionary key")
            
            # Parse value
            value = self._parse_expression()
            
            # Store the pair
            # For now, we'll evaluate the key at parse time if it's a literal
            if isinstance(key, LiteralNode):
                pairs[key.value] = value
            else:
                # For non-literal keys, we'll need runtime evaluation
                # This is a simplified implementation
                raise ParseError("Dictionary keys must be literal values", filename=self.filename)
            
            if self._match('COMMA'):
                self._advance()
            else:
                break
        
        return pairs

    def _parse_indexing(self, expr: object) -> 'IndexNode':
        """Parse indexing operation (e.g., list[0], dict["key"])."""
        self._consume('LBRACKET', "Expected '['")
        
        index = self._parse_expression()
        
        self._consume('RBRACKET', "Expected ']'")
        
        return IndexNode(object=expr, index=index)

    def _parse_postfix_operations(self, expr: object) -> object:
        """Parse postfix operations like indexing, member access, and function calls."""
        while True:
            if self._match('LBRACKET'):
                # Indexing operation
                expr = self._parse_indexing(expr)
            elif self._match('DOT'):
                # Member access
                self._advance()  # consume '.'
                member_token = self._consume('IDENTIFIER', "Expected member name after '.'")
                expr = MemberAccessNode(object=expr, member=member_token.value)
            elif self._match('LPAREN'):
                # Function call
                expr = self._parse_call_on_expression(expr)
            else:
                break
        
        return expr

    def _unescape_string(self, s: str) -> str:
        """Unescape string content."""
        result = []
        i = 0
        while i < len(s):
            if s[i] == '\\' and i + 1 < len(s):
                next_char = s[i + 1]
                if next_char == 'n':
                    result.append('\n')
                elif next_char == 't':
                    result.append('\t')
                elif next_char == 'r':
                    result.append('\r')
                elif next_char == '\\':
                    result.append('\\')
                elif next_char == '"':
                    result.append('"')
                else:
                    # Unknown escape sequence, keep as is
                    result.append(s[i])
                    result.append(next_char)
                i += 2
            else:
                result.append(s[i])
                i += 1
        return ''.join(result)


def parse(source: str, filename: str = None) -> ProgramNode:
    """Parse source code into a ProgramNode.

    Args:
        source: The source code to parse
        filename: Optional filename for error reporting

    Returns:
        ProgramNode representing the parsed program
    """
    from lyric.lexer import tokenize
    tokens = tokenize(source, filename)
    parser = Parser(tokens, filename)
    return parser.parse()
