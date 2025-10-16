"""
Tests for the parser module.
"""

import pytest
from lyric.ast import (
    ProgramNode, FunctionNode, IfNode, ElifNode, LoopNode, AssignNode,
    CallNode, BinaryOpNode, UnaryOpNode, LiteralNode, IdentifierNode,
    ClassNode, PrintNode, ImportNode, ReturnNode, TryNode, ExceptNode
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
        assert repr(node) == "AssignNode(name='x', expr=LiteralNode(value=42))"
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
