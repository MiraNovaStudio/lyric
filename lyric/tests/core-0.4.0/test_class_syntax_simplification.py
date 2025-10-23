"""Tests for Sprint 4 Pivot 4.1: Class syntax simplification - colonless syntax only."""

import pytest
import io
import sys
from lyric.parser import parse
from lyric.interpreter import evaluate
from lyric.ast_nodes import ClassNode
from lyric.errors import SyntaxErrorLyric


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


def test_class_with_colon_syntax_rejected():
    """Test that class declarations with colons are properly rejected."""
    source = """class TestClass:
    name = "test"
    def greet() {
        return "Hello from " + self.name
    }
+++"""
    
    with pytest.raises(SyntaxErrorLyric, match="Expected expression"):
        parse(source)


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


def test_empty_class():
    """Test empty classes."""
    source = """class EmptyClass
+++"""
    
    # Should parse successfully
    ast = parse(source)
    
    # Should be empty class
    assert len(ast.statements[0].members_statements) == 0


def test_class_with_methods():
    """Test classes with methods."""
    source = """class Calculator
    def add(a, b) {
        return a + b
    }
    def multiply(a, b) {
        return a * b
    }
+++"""
    
    # Should parse successfully
    ast = parse(source)
    
    # Should have 2 methods
    assert len(ast.statements[0].members_statements) == 2


def test_class_instantiation_works():
    """Test that class instantiation works."""
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


def test_class_with_init_method():
    """Test classes with init methods."""
    source = """class Person
    def init(name) {
        self.name = name
    }
+++

def main() {
    person = Person("Alice")
    return person.name
}"""
    
    # Should work
    ast = parse(source)
    result = evaluate(ast)
    assert result == "Alice"


def test_multiple_classes():
    """Test multiple class declarations."""
    source = """class Person
    name = "Default"
+++

class Student
    grade = "A"
+++

def main() {
    person = Person()
    student = Student()
    return person.name + " " + student.grade
}"""
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == "Default A"
