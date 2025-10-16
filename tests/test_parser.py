"""
Tests for the parser module.
"""

import pytest
from lyric.ast import (
    ProgramNode, FunctionNode, IfNode, ElifNode, LoopNode, AssignNode,
    CallNode, BinaryOpNode, UnaryOpNode, LiteralNode, IdentifierNode,
    ClassNode, PrintNode, ImportNode, ReturnNode, TryNode, ExceptNode, MemberAccessNode
)


class TestASTNodes:
    """Test AST node instantiation and pretty-printing."""
    
    def test_program_node(self):
        """Test ProgramNode instantiation and representation."""
        node = ProgramNode(statements=[])
        assert repr(node) == "ProgramNode(statements=0 items)"
        
        # Test with statements
        statements = [IdentifierNode("x"), LiteralNode(42)]
        node = ProgramNode(statements=statements)
        assert repr(node) == "ProgramNode(statements=2 items)"
        assert node.statements == statements
        
        # Test to_dict
        result = node.to_dict()
        assert result['statements'][0]['name'] == 'x'
        assert result['statements'][1]['value'] == 42
    
    def test_function_node(self):
        """Test FunctionNode instantiation and representation."""
        node = FunctionNode(
            name="main",
            params=[],
            body_statements=[PrintNode([LiteralNode("Hello")])]
        )
        assert repr(node) == "FunctionNode(name='main', params=[], body=1 statements)"
        
        # Test with parameters
        node = FunctionNode(
            name="add",
            params=["x", "y"],
            body_statements=[ReturnNode(BinaryOpNode("+", IdentifierNode("x"), IdentifierNode("y")))]
        )
        assert repr(node) == "FunctionNode(name='add', params=['x', 'y'], body=1 statements)"
        assert node.params == ["x", "y"]
    
    def test_if_node(self):
        """Test IfNode instantiation and representation."""
        condition = BinaryOpNode(">", IdentifierNode("x"), LiteralNode(0))
        then_body = [PrintNode([LiteralNode("positive")])]
        
        node = IfNode(
            condition=condition,
            then_body=then_body,
            elifs=[],
            else_body=None
        )
        assert repr(node) == "IfNode(condition=BinaryOpNode(op='>', left=IdentifierNode(name='x'), right=LiteralNode(value=0)), then=1 statements, elifs=0)"
        
        # Test with else body
        else_body = [PrintNode([LiteralNode("negative")])]
        node.else_body = else_body
        assert "else=1 statements" in repr(node)
    
    def test_elif_node(self):
        """Test ElifNode instantiation and representation."""
        condition = BinaryOpNode("<", IdentifierNode("x"), LiteralNode(0))
        body = [PrintNode([LiteralNode("negative")])]
        
        node = ElifNode(condition=condition, body=body)
        assert repr(node) == "ElifNode(condition=BinaryOpNode(op='<', left=IdentifierNode(name='x'), right=LiteralNode(value=0)), body=1 statements)"
    
    def test_loop_node(self):
        """Test LoopNode instantiation and representation."""
        # Iterator loop
        condition = IdentifierNode("item")
        body = [PrintNode([IdentifierNode("item")])]
        
        node = LoopNode(
            condition_or_iter=condition,
            loop_kind="iterator",
            body=body
        )
        assert repr(node) == "LoopNode(kind='iterator', condition=IdentifierNode(name='item'), body=1 statements)"
        
        # While loop
        condition = BinaryOpNode(">", IdentifierNode("x"), LiteralNode(0))
        node = LoopNode(
            condition_or_iter=condition,
            loop_kind="while",
            body=body
        )
        assert repr(node) == "LoopNode(kind='while', condition=BinaryOpNode(op='>', left=IdentifierNode(name='x'), right=LiteralNode(value=0)), body=1 statements)"
    
    def test_assign_node(self):
        """Test AssignNode instantiation and representation."""
        node = AssignNode(
            name="x",
            expr=LiteralNode(42)
        )
        assert repr(node) == "AssignNode(name=x, expr=LiteralNode(value=42))"
        assert node.name == "x"
        assert node.expr == LiteralNode(42)
    
    def test_call_node(self):
        """Test CallNode instantiation and representation."""
        args = [LiteralNode("Hello"), IdentifierNode("name")]
        node = CallNode(func_name="print", args=args)
        assert repr(node) == "CallNode(func='print', args=2 items)"
        assert node.func_name == "print"
        assert node.args == args
    
    def test_binary_op_node(self):
        """Test BinaryOpNode instantiation and representation."""
        left = IdentifierNode("x")
        right = LiteralNode(5)
        
        node = BinaryOpNode(op="+", left=left, right=right)
        assert repr(node) == "BinaryOpNode(op='+', left=IdentifierNode(name='x'), right=LiteralNode(value=5))"
        assert node.op == "+"
        assert node.left == left
        assert node.right == right
    
    def test_unary_op_node(self):
        """Test UnaryOpNode instantiation and representation."""
        operand = IdentifierNode("x")
        node = UnaryOpNode(op="!", operand=operand)
        assert repr(node) == "UnaryOpNode(op='!', operand=IdentifierNode(name='x'))"
        assert node.op == "!"
        assert node.operand == operand
    
    def test_literal_node(self):
        """Test LiteralNode instantiation and representation."""
        # Integer
        node = LiteralNode(42)
        assert repr(node) == "LiteralNode(value=42)"
        assert node.value == 42
        
        # String
        node = LiteralNode("hello")
        assert repr(node) == "LiteralNode(value='hello')"
        
        # Float
        node = LiteralNode(3.14)
        assert repr(node) == "LiteralNode(value=3.14)"
        
        # Boolean
        node = LiteralNode(True)
        assert repr(node) == "LiteralNode(value=True)"
    
    def test_identifier_node(self):
        """Test IdentifierNode instantiation and representation."""
        node = IdentifierNode("my_variable")
        assert repr(node) == "IdentifierNode(name='my_variable')"
        assert node.name == "my_variable"
    
    def test_class_node(self):
        """Test ClassNode instantiation and representation."""
        members = [
            AssignNode("name", LiteralNode("Player")),
            FunctionNode("greet", [], [PrintNode([LiteralNode("Hello")])])
        ]
        
        node = ClassNode(name="Player", members_statements=members)
        assert repr(node) == "ClassNode(name='Player', members=2 items)"
        assert node.name == "Player"
        assert node.members_statements == members
    
    def test_print_node(self):
        """Test PrintNode instantiation and representation."""
        args = [LiteralNode("Hello"), IdentifierNode("name")]
        node = PrintNode(args=args)
        assert repr(node) == "PrintNode(args=2 items)"
        assert node.args == args
    
    def test_import_node(self):
        """Test ImportNode instantiation and representation."""
        # Simple import
        node = ImportNode(module="math")
        assert repr(node) == "ImportNode(module='math')"
        
        # Import with alias
        node = ImportNode(module="os", alias="system")
        assert repr(node) == "ImportNode(module='os', alias='system')"
        
        # Import specific items
        node = ImportNode(module="random", items=["randint", "choice"])
        assert repr(node) == "ImportNode(module='random', items=['randint', 'choice'])"
    
    def test_return_node(self):
        """Test ReturnNode instantiation and representation."""
        # Return with expression
        expr = BinaryOpNode("+", IdentifierNode("x"), LiteralNode(1))
        node = ReturnNode(expr=expr)
        assert repr(node) == "ReturnNode(expr=BinaryOpNode(op='+', left=IdentifierNode(name='x'), right=LiteralNode(value=1)))"
        
        # Return without expression
        node = ReturnNode(expr=None)
        assert repr(node) == "ReturnNode(expr=None)"
    
    def test_try_node(self):
        """Test TryNode instantiation and representation."""
        try_body = [CallNode("risky_function", [])]
        except_clauses = [ExceptNode("ValueError", [PrintNode([LiteralNode("Error occurred")])])]
        
        node = TryNode(
            try_body=try_body,
            except_clauses=except_clauses,
            finally_body=None
        )
        assert repr(node) == "TryNode(try=1 statements, excepts=1)"
        
        # With finally
        finally_body = [PrintNode([LiteralNode("Cleanup")])]
        node.finally_body = finally_body
        assert "finally=1 statements" in repr(node)
    
    def test_except_node(self):
        """Test ExceptNode instantiation and representation."""
        body = [PrintNode([LiteralNode("Handled error")])]
        node = ExceptNode(exception_type="ValueError", body=body)
        assert repr(node) == "ExceptNode(type='ValueError', body=1 statements)"
        
        # Generic except
        node = ExceptNode(exception_type=None, body=body)
        assert repr(node) == "ExceptNode(type='None', body=1 statements)"
    
    def test_complex_ast_structure(self):
        """Test a complex AST structure with nested nodes."""
        # Create a complex program AST
        program = ProgramNode(statements=[
            ImportNode("math"),
            FunctionNode(
                name="main",
                params=[],
                body_statements=[
                    AssignNode("x", BinaryOpNode("+", LiteralNode(5), LiteralNode(3))),
                    IfNode(
                        condition=BinaryOpNode(">", IdentifierNode("x"), LiteralNode(7)),
                        then_body=[PrintNode([LiteralNode("x is greater than 7")])],
                        elifs=[
                            ElifNode(
                                condition=BinaryOpNode("==", IdentifierNode("x"), LiteralNode(8)),
                                body=[PrintNode([LiteralNode("x equals 8")])]
                            )
                        ],
                        else_body=[PrintNode([LiteralNode("x is less than or equal to 7")])]
                    ),
                    LoopNode(
                        condition_or_iter=BinaryOpNode(">", IdentifierNode("x"), LiteralNode(0)),
                        loop_kind="while",
                        body=[
                            PrintNode([IdentifierNode("x")]),
                            AssignNode("x", BinaryOpNode("-", IdentifierNode("x"), LiteralNode(1)))
                        ]
                    )
                ]
            )
        ])
        
        # Test that it can be represented
        assert repr(program) == "ProgramNode(statements=2 items)"
        
        # Test to_dict conversion
        result = program.to_dict()
        assert result['statements'][0]['module'] == 'math'
        assert result['statements'][1]['name'] == 'main'
        
        # Test nested structure
        main_func = program.statements[1]
        assert repr(main_func) == "FunctionNode(name='main', params=[], body=3 statements)"
        
        # Test the if statement
        if_stmt = main_func.body_statements[1]
        assert "IfNode" in repr(if_stmt)
        assert len(if_stmt.elifs) == 1
        
        print("Complex AST structure created and verified successfully!")
        print(f"Program: {repr(program)}")
        print(f"Main function: {repr(main_func)}")
        print(f"If statement: {repr(if_stmt)}")


class TestParser:
    """Test cases for the Lyric parser."""
    
    def test_parse_function_def(self):
        """Test parsing function definition."""
        source = 'def main() { print("Hello, Lyric!") }'
        
        from lyric.parser import parse
        program = parse(source)
        
        # Verify program structure
        assert isinstance(program, ProgramNode)
        assert len(program.statements) == 1
        
        # Verify function
        func = program.statements[0]
        assert isinstance(func, FunctionNode)
        assert func.name == "main"
        assert func.params == []
        assert len(func.body_statements) == 1
        
        # Verify print call
        print_call = func.body_statements[0]
        assert isinstance(print_call, CallNode)
        assert print_call.func_name == "print"
        assert len(print_call.args) == 1
        assert isinstance(print_call.args[0], LiteralNode)
        assert print_call.args[0].value == "Hello, Lyric!"
    
    def test_parse_if_else_example(self):
        """Test parsing if/else example from spec."""
        source = '''if x > 0:
    print("positive")
else if x < 0:
    print("negative")
else:
    print("zero")
end'''
        
        from lyric.parser import parse
        program = parse(source)
        
        # Verify program structure
        assert isinstance(program, ProgramNode)
        assert len(program.statements) == 1
        
        # Verify if statement
        if_stmt = program.statements[0]
        assert isinstance(if_stmt, IfNode)
        
        # Verify condition
        assert isinstance(if_stmt.condition, BinaryOpNode)
        assert if_stmt.condition.op == ">"
        assert isinstance(if_stmt.condition.left, IdentifierNode)
        assert if_stmt.condition.left.name == "x"
        assert isinstance(if_stmt.condition.right, LiteralNode)
        assert if_stmt.condition.right.value == 0
        
        # Verify then body
        assert len(if_stmt.then_body) == 1
        print_call = if_stmt.then_body[0]
        assert isinstance(print_call, CallNode)
        assert print_call.func_name == "print"
        assert print_call.args[0].value == "positive"
        
        # Verify elif
        assert len(if_stmt.elifs) == 1
        elif_stmt = if_stmt.elifs[0]
        assert isinstance(elif_stmt.condition, BinaryOpNode)
        assert elif_stmt.condition.op == "<"
        assert len(elif_stmt.body) == 1
        
        # Verify else
        assert if_stmt.else_body is not None
        assert len(if_stmt.else_body) == 1
        else_print = if_stmt.else_body[0]
        assert isinstance(else_print, CallNode)
        assert else_print.args[0].value == "zero"
    
    def test_parse_loop_example(self):
        """Test parsing given/done loop example."""
        source = '''given i in range(3):
    print(i)
done'''
        
        from lyric.parser import parse
        program = parse(source)
        
        # Verify program structure
        assert isinstance(program, ProgramNode)
        assert len(program.statements) == 1
        
        # Verify loop
        loop = program.statements[0]
        assert isinstance(loop, LoopNode)
        assert loop.loop_kind == "iterator"
        
        # Verify iterator expression
        iter_expr = loop.condition_or_iter
        assert isinstance(iter_expr, BinaryOpNode)
        assert iter_expr.op == "in"
        assert isinstance(iter_expr.left, IdentifierNode)
        assert iter_expr.left.name == "i"
        assert isinstance(iter_expr.right, CallNode)
        assert iter_expr.right.func_name == "range"
        assert len(iter_expr.right.args) == 1
        assert isinstance(iter_expr.right.args[0], LiteralNode)
        assert iter_expr.right.args[0].value == 3
        
        # Verify loop body
        assert len(loop.body) == 1
        print_call = loop.body[0]
        assert isinstance(print_call, CallNode)
        assert print_call.func_name == "print"
        assert len(print_call.args) == 1
        assert isinstance(print_call.args[0], IdentifierNode)
        assert print_call.args[0].name == "i"
    
    def test_parse_class_example(self):
        """Test parsing class definition example."""
        source = '''class Player:
    name = "Guest"
    def greet() {
        print("Hello,", self.name)
    }
+++'''
        
        from lyric.parser import parse
        program = parse(source)
        
        # Verify program structure
        assert isinstance(program, ProgramNode)
        assert len(program.statements) == 1
        
        # Verify class
        class_def = program.statements[0]
        assert isinstance(class_def, ClassNode)
        assert class_def.name == "Player"
        assert len(class_def.members_statements) == 2
        
        # Verify first member (assignment)
        name_assign = class_def.members_statements[0]
        assert isinstance(name_assign, AssignNode)
        assert isinstance(name_assign.name, IdentifierNode)
        assert name_assign.name.name == "name"
        assert isinstance(name_assign.expr, LiteralNode)
        assert name_assign.expr.value == "Guest"
        
        # Verify second member (function)
        greet_func = class_def.members_statements[1]
        assert isinstance(greet_func, FunctionNode)
        assert greet_func.name == "greet"
        assert greet_func.params == []
        assert len(greet_func.body_statements) == 1
        
        # Verify print call in function
        print_call = greet_func.body_statements[0]
        assert isinstance(print_call, CallNode)
        assert print_call.func_name == "print"
        assert len(print_call.args) == 2
        assert print_call.args[0].value == "Hello,"
        assert isinstance(print_call.args[1], MemberAccessNode)
        assert isinstance(print_call.args[1].object, IdentifierNode)
        assert print_call.args[1].object.name == "self"
        assert print_call.args[1].member == "name"
    
    def test_parse_assignment(self):
        """Test parsing assignment statements."""
        source = 'x = 42'
        
        from lyric.parser import parse
        program = parse(source)
        
        assert isinstance(program, ProgramNode)
        assert len(program.statements) == 1
        
        assign = program.statements[0]
        assert isinstance(assign, AssignNode)
        assert isinstance(assign.name, IdentifierNode)
        assert assign.name.name == "x"
        assert isinstance(assign.expr, LiteralNode)
        assert assign.expr.value == 42
    
    def test_parse_expression_precedence(self):
        """Test operator precedence in expressions."""
        source = 'x = 1 + 2 * 3'
        
        from lyric.parser import parse
        program = parse(source)
        
        assign = program.statements[0]
        expr = assign.expr
        
        # Should be parsed as 1 + (2 * 3), not (1 + 2) * 3
        assert isinstance(expr, BinaryOpNode)
        assert expr.op == "+"
        assert isinstance(expr.left, LiteralNode)
        assert expr.left.value == 1
        
        right_mult = expr.right
        assert isinstance(right_mult, BinaryOpNode)
        assert right_mult.op == "*"
        assert right_mult.left.value == 2
        assert right_mult.right.value == 3
    
    def test_parse_function_call(self):
        """Test parsing function calls."""
        source = 'print("hello", "world")'
        
        from lyric.parser import parse
        program = parse(source)
        
        call = program.statements[0]
        assert isinstance(call, CallNode)
        assert call.func_name == "print"
        assert len(call.args) == 2
        assert call.args[0].value == "hello"
        assert call.args[1].value == "world"
    
    def test_parse_comparison_operators(self):
        """Test parsing comparison operators."""
        source = 'x = a > b and c == d'
        
        from lyric.parser import parse
        program = parse(source)
        
        assign = program.statements[0]
        expr = assign.expr
        
        # Should be parsed as (a > b) and (c == d)
        assert isinstance(expr, BinaryOpNode)
        assert expr.op == "and"
        
        left_comp = expr.left
        assert isinstance(left_comp, BinaryOpNode)
        assert left_comp.op == ">"
        
        right_comp = expr.right
        assert isinstance(right_comp, BinaryOpNode)
        assert right_comp.op == "=="
    
    def test_parse_while_loop(self):
        """Test parsing while-like loop."""
        source = '''given x > 0:
    print(x)
    x = x - 1
done'''
        
        from lyric.parser import parse
        program = parse(source)
        
        loop = program.statements[0]
        assert isinstance(loop, LoopNode)
        assert loop.loop_kind == "while"
        
        # Verify condition
        condition = loop.condition_or_iter
        assert isinstance(condition, BinaryOpNode)
        assert condition.op == ">"
        
        # Verify body
        assert len(loop.body) == 2
        assert isinstance(loop.body[0], CallNode)
        assert isinstance(loop.body[1], AssignNode)
    
    def test_parse_multiple_elif(self):
        """Test parsing multiple elif clauses."""
        source = '''if x == 1:
    print("one")
else if x == 2:
    print("two")
else if x == 3:
    print("three")
else:
    print("other")
end'''
        
        from lyric.parser import parse
        program = parse(source)
        
        if_stmt = program.statements[0]
        assert isinstance(if_stmt, IfNode)
        
        # Should have 2 elifs
        assert len(if_stmt.elifs) == 2
        
        # Verify first elif
        elif1 = if_stmt.elifs[0]
        assert isinstance(elif1.condition, BinaryOpNode)
        assert elif1.condition.op == "=="
        assert elif1.condition.right.value == 2
        
        # Verify second elif
        elif2 = if_stmt.elifs[1]
        assert isinstance(elif2.condition, BinaryOpNode)
        assert elif2.condition.right.value == 3
        
        # Verify else
        assert if_stmt.else_body is not None
        assert len(if_stmt.else_body) == 1
