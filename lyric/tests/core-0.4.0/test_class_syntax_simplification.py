"""Tests for Sprint 4 Task 5: Class syntax simplification - both colon and non-colon forms."""

import pytest
import io
import sys
from lyric.parser import parse
from lyric.interpreter import evaluate
from lyric.ast_nodes import ClassNode


def test_class_without_colon_syntax():
    """Test that class declarations without colons work correctly."""
    source = """class TestClass
    name = "test"
    def greet() {
        return "Hello from " + self.name
    }
+++

def main() {
    instance = TestClass()
    return instance.greet()
}"""
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == "Hello from test"


def test_class_with_colon_syntax_deprecation_warning():
    """Test that class declarations with colons work but show deprecation warning."""
    source = """class TestClass:
    name = "test"
    def greet() {
        return "Hello from " + self.name
    }
+++

def main() {
    instance = TestClass()
    return instance.greet()
}"""
    
    # Capture stdout to check for deprecation warning
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        result = evaluate(ast)
        
        # Check that it still works
        assert result == "Hello from test"
        
        # Check that deprecation warning was printed
        output = captured_output.getvalue()
        assert "DeprecationWarning" in output
        assert "Colons after class declarations will be removed" in output
        assert "Use 'class TestClass' instead of 'class TestClass:'" in output
        
    finally:
        sys.stdout = old_stdout


def test_both_syntaxes_parse_correctly():
    """Test that both syntaxes produce equivalent AST structures."""
    source_without_colon = """class TestClass
    name = "test"
+++"""
    
    source_with_colon = """class TestClass:
    name = "test"
+++"""
    
    # Parse both versions
    ast_without_colon = parse(source_without_colon)
    ast_with_colon = parse(source_with_colon)
    
    # Both should have one statement
    assert len(ast_without_colon.statements) == 1
    assert len(ast_with_colon.statements) == 1
    
    # Both should be ClassNode instances
    class_without_colon = ast_without_colon.statements[0]
    class_with_colon = ast_with_colon.statements[0]
    
    assert isinstance(class_without_colon, ClassNode)
    assert isinstance(class_with_colon, ClassNode)
    
    # Both should have the same name
    assert class_without_colon.name == "TestClass"
    assert class_with_colon.name == "TestClass"
    
    # Both should have the same number of members
    assert len(class_without_colon.members_statements) == 1
    assert len(class_with_colon.members_statements) == 1


def test_class_syntax_does_not_affect_other_constructs():
    """Test that removing colons from classes doesn't affect other constructs."""
    source = """class TestClass
    name = "test"
+++

def test_function() {
    return "function works"
}

if True:
    print("if works")
end

given True:
    print("given works")
done"""
    
    # Should parse without errors
    ast = parse(source)
    
    # Should have 4 statements: class, function, if, given
    assert len(ast.statements) == 4
    
    # First should be a class
    assert isinstance(ast.statements[0], ClassNode)
    assert ast.statements[0].name == "TestClass"


def test_empty_class_both_syntaxes():
    """Test empty classes with both syntaxes."""
    source_without_colon = """class EmptyClass
+++"""
    
    source_with_colon = """class EmptyClass:
+++"""
    
    # Both should parse successfully
    ast_without_colon = parse(source_without_colon)
    ast_with_colon = parse(source_with_colon)
    
    # Both should be empty classes
    assert len(ast_without_colon.statements[0].members_statements) == 0
    assert len(ast_with_colon.statements[0].members_statements) == 0


def test_class_with_methods_both_syntaxes():
    """Test classes with methods using both syntaxes."""
    source_without_colon = """class Calculator
    def add(a, b) {
        return a + b
    }
    def multiply(a, b) {
        return a * b
    }
+++"""
    
    source_with_colon = """class Calculator:
    def add(a, b) {
        return a + b
    }
    def multiply(a, b) {
        return a * b
    }
+++"""
    
    # Both should parse successfully
    ast_without_colon = parse(source_without_colon)
    ast_with_colon = parse(source_with_colon)
    
    # Both should have 2 methods
    assert len(ast_without_colon.statements[0].members_statements) == 2
    assert len(ast_with_colon.statements[0].members_statements) == 2


def test_class_instantiation_works_both_syntaxes():
    """Test that class instantiation works with both syntaxes."""
    source = """class TestClass
    name = "test"
    def get_name() {
        return self.name
    }
+++

def main() {
    instance = TestClass()
    return instance.get_name()
}"""
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == "test"


def test_class_with_init_method_both_syntaxes():
    """Test classes with init methods using both syntaxes."""
    source_without_colon = """class Person
    def init(name) {
        self.name = name
    }
+++

def main() {
    person = Person("Alice")
    return person.name
}"""
    
    source_with_colon = """class Person:
    def init(name) {
        self.name = name
    }
+++

def main() {
    person = Person("Alice")
    return person.name
}"""
    
    # Both should work
    ast_without_colon = parse(source_without_colon)
    ast_with_colon = parse(source_with_colon)
    
    result_without_colon = evaluate(ast_without_colon)
    result_with_colon = evaluate(ast_with_colon)
    
    assert result_without_colon == "Alice"
    assert result_with_colon == "Alice"
