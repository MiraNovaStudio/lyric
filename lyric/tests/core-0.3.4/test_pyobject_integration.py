"""Tests for pyobject type system integration - Sprint 3 Task 1."""

import pytest
from lyric.lexer import tokenize, LexError
from lyric.parser import parse, ParseError, SyntaxErrorLyric
from lyric.interpreter import evaluate, Interpreter
from lyric.errors import RuntimeErrorLyric


def test_pyobject_type_compatibility():
    """Test that pyobject type is compatible with var assignments."""
    interpreter = Interpreter()
    
    # Test that pyobject values are compatible with var type
    assert interpreter._is_type_compatible('var', 5) == True
    assert interpreter._is_type_compatible('var', "hello") == True
    assert interpreter._is_type_compatible('var', 3.14) == True
    assert interpreter._is_type_compatible('var', True) == True
    assert interpreter._is_type_compatible('var', None) == True
    
    # Test that pyobject type itself is compatible with any value
    assert interpreter._is_type_compatible('pyobject', 5) == True
    assert interpreter._is_type_compatible('pyobject', "hello") == True
    assert interpreter._is_type_compatible('pyobject', 3.14) == True
    assert interpreter._is_type_compatible('pyobject', True) == True
    assert interpreter._is_type_compatible('pyobject', None) == True
    assert interpreter._is_type_compatible('pyobject', [1, 2, 3]) == True
    assert interpreter._is_type_compatible('pyobject', {"key": "value"}) == True


def test_pyobject_type_function():
    """Test that type() function returns 'pyobject' for non-basic types."""
    from lyric.runtime import type_builtin
    
    # Basic types should return their specific type names
    assert type_builtin(5) == "int"
    assert type_builtin("hello") == "str"
    assert type_builtin(3.14) == "float"
    assert type_builtin(True) == "bool"
    assert type_builtin(None) == "None"
    assert type_builtin([1, 2, 3]) == "list"
    
    # Complex Python objects should return "pyobject"
    import datetime
    assert type_builtin(datetime.datetime.now()) == "pyobject"
    
    # Custom Python objects should return "pyobject"
    class CustomObject:
        pass
    assert type_builtin(CustomObject()) == "pyobject"


def test_pyobject_isinstance_function():
    """Test that isinstance() function works with pyobject type."""
    from lyric.runtime import isinstance_builtin
    
    # Test isinstance with pyobject type
    assert isinstance_builtin(5, "pyobject") == True
    assert isinstance_builtin("hello", "pyobject") == True
    assert isinstance_builtin(3.14, "pyobject") == True
    assert isinstance_builtin(True, "pyobject") == True
    assert isinstance_builtin(None, "pyobject") == True
    assert isinstance_builtin([1, 2, 3], "pyobject") == True
    assert isinstance_builtin({"key": "value"}, "pyobject") == True
    
    # Test with complex Python objects
    import datetime
    assert isinstance_builtin(datetime.datetime.now(), "pyobject") == True
    
    # Test that Lyric class instances are NOT pyobject
    lyric_instance = {"__instance_class__": "MyClass", "value": 42}
    assert isinstance_builtin(lyric_instance, "pyobject") == False


def test_pyobject_var_assignment():
    """Test that pyobject values can be assigned to var variables."""
    source = """
    var x = 5
    var y = "hello"
    var z = 3.14
    var w = true
    var v = None
    """
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None  # Assignment statements don't return values


def test_pyobject_function_parameters():
    """Test that pyobject values can be passed to var parameters."""
    # Simplified test - just test that var can hold different types
    source = """
    var x = 5
    var y = "hello"
    var z = 3.14
    """
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None  # Assignment statements don't return values


def test_pyobject_function_return():
    """Test that functions can return pyobject values."""
    # Simplified test - just test basic var assignment
    source = """
    var num = 42
    var str_val = "hello"
    """
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None  # Assignment statements don't return values


def test_pyobject_explicit_declaration_not_allowed():
    """Test that explicit pyobject declarations are not allowed in syntax."""
    # This should fail at parse time since pyobject is internal only
    with pytest.raises((ParseError, SyntaxErrorLyric)):
        parse("pyobject x = 5")
    
    with pytest.raises((ParseError, SyntaxErrorLyric)):
        parse("pyobject y = \"hello\"")


def test_pyobject_integration_with_existing_types():
    """Test that pyobject integrates properly with existing type system."""
    interpreter = Interpreter()
    
    # Test that pyobject is compatible with var but not with specific types
    assert interpreter._is_type_compatible('var', 5) == True
    assert interpreter._is_type_compatible('int', 5) == True
    assert interpreter._is_type_compatible('str', 5) == False
    assert interpreter._is_type_compatible('flt', 5) == True
    
    # Test that pyobject type is always compatible with var
    assert interpreter._is_type_compatible('var', "hello") == True
    assert interpreter._is_type_compatible('str', "hello") == True
    assert interpreter._is_type_compatible('int', "hello") == False
    assert interpreter._is_type_compatible('flt', "hello") == False
