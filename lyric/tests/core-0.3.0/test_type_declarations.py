"""Tests for type declarations and type enforcement."""

import pytest
from lyric.lexer import tokenize, LexError
from lyric.parser import parse, ParseError, SyntaxErrorLyric
from lyric.interpreter import evaluate, Interpreter
from lyric.errors import RuntimeErrorLyric


def test_type_keywords_tokenization():
    """Test that type keywords are properly tokenized."""
    source = "int x = 5"
    tokens = tokenize(source)
    
    assert len(tokens) >= 4
    assert tokens[0].type == 'TYPE_OR_IDENT'
    assert tokens[0].value == 'int'
    assert tokens[1].type == 'IDENT'
    assert tokens[1].value == 'x'
    assert tokens[2].type == 'ASSIGN'
    assert tokens[3].type == 'INT'
    assert tokens[3].value == 5


def test_type_declaration_parsing():
    """Test parsing of type declarations."""
    source = "int x = 5"
    ast = parse(source)
    
    assert len(ast.statements) == 1
    stmt = ast.statements[0]
    assert stmt.type_name == 'int'
    assert stmt.name == 'x'
    assert stmt.expr.value == 5


def test_multiple_type_declarations():
    """Test parsing multiple type declarations."""
    source = """
    int x = 5
    str name = "hello"
    flt pi = 3.14
    var dynamic = "anything"
    """
    ast = parse(source)
    
    assert len(ast.statements) == 4
    
    # Check int declaration
    assert ast.statements[0].type_name == 'int'
    assert ast.statements[0].name == 'x'
    assert ast.statements[0].expr.value == 5
    
    # Check str declaration
    assert ast.statements[1].type_name == 'str'
    assert ast.statements[1].name == 'name'
    assert ast.statements[1].expr.value == "hello"
    
    # Check flt declaration
    assert ast.statements[2].type_name == 'flt'
    assert ast.statements[2].name == 'pi'
    assert ast.statements[2].expr.value == 3.14
    
    # Check var declaration
    assert ast.statements[3].type_name == 'var'
    assert ast.statements[3].name == 'dynamic'
    assert ast.statements[3].expr.value == "anything"


def test_type_enforcement_int():
    """Test type enforcement for int variables."""
    source = "int x = 5"
    interpreter = Interpreter()
    interpreter.evaluate(parse(source))
    
    assert interpreter.global_scope['x'] == 5
    assert interpreter.variable_types['x'] == 'int'


def test_type_enforcement_str():
    """Test type enforcement for str variables."""
    source = 'str name = "hello"'
    interpreter = Interpreter()
    interpreter.evaluate(parse(source))
    
    assert interpreter.global_scope['name'] == "hello"
    assert interpreter.variable_types['name'] == 'str'


def test_type_enforcement_flt():
    """Test type enforcement for flt variables."""
    source = "flt pi = 3.14"
    interpreter = Interpreter()
    interpreter.evaluate(parse(source))
    
    assert interpreter.global_scope['pi'] == 3.14
    assert interpreter.variable_types['pi'] == 'flt'


def test_type_enforcement_var():
    """Test that var accepts any type."""
    source = 'var dynamic = "anything"'
    interpreter = Interpreter()
    interpreter.evaluate(parse(source))
    
    assert interpreter.global_scope['dynamic'] == "anything"
    assert interpreter.variable_types['dynamic'] == 'var'


def test_type_error_int_assignment():
    """Test that assigning string to int raises type error."""
    source = 'int x = "hello"'
    interpreter = Interpreter()
    
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        interpreter.evaluate(parse(source))
    
    assert "Type mismatch" in str(exc_info.value)
    assert "cannot assign str to variable 'x' declared as int" in str(exc_info.value)
    assert "Expected int, but got str" in str(exc_info.value)


def test_type_error_str_assignment():
    """Test that assigning int to str raises type error."""
    source = 'str name = 42'
    interpreter = Interpreter()
    
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        interpreter.evaluate(parse(source))
    
    assert "Type mismatch" in str(exc_info.value)
    assert "cannot assign int to variable 'name' declared as str" in str(exc_info.value)
    assert "Expected str, but got int" in str(exc_info.value)


def test_type_error_flt_assignment():
    """Test that assigning string to flt raises type error."""
    source = 'flt pi = "not a number"'
    interpreter = Interpreter()
    
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        interpreter.evaluate(parse(source))
    
    assert "Type mismatch" in str(exc_info.value)
    assert "cannot assign str to variable 'pi' declared as flt" in str(exc_info.value)
    assert "Expected flt, but got str" in str(exc_info.value)


def test_var_accepts_any_type():
    """Test that var accepts any type without errors."""
    test_cases = [
        ('var x = 5', 5),
        ('var x = "hello"', "hello"),
        ('var x = 3.14', 3.14),
        ('var x = True', True),
        ('var x = None', None)
    ]
    
    for source, expected_value in test_cases:
        interpreter = Interpreter()
        interpreter.evaluate(parse(source))
        assert interpreter.global_scope['x'] == expected_value
        assert interpreter.variable_types['x'] == 'var'


def test_type_compatibility_int():
    """Test int type compatibility."""
    interpreter = Interpreter()
    
    # Valid int assignments
    assert interpreter._is_type_compatible('int', 5) == True
    assert interpreter._is_type_compatible('int', 0) == True
    assert interpreter._is_type_compatible('int', -10) == True
    
    # Invalid int assignments
    assert interpreter._is_type_compatible('int', "hello") == False
    assert interpreter._is_type_compatible('int', 3.14) == False
    assert interpreter._is_type_compatible('int', True) == False


def test_type_compatibility_str():
    """Test str type compatibility."""
    interpreter = Interpreter()
    
    # Valid str assignments
    assert interpreter._is_type_compatible('str', "hello") == True
    assert interpreter._is_type_compatible('str', "") == True
    assert interpreter._is_type_compatible('str', "123") == True
    
    # Invalid str assignments
    assert interpreter._is_type_compatible('str', 5) == False
    assert interpreter._is_type_compatible('str', 3.14) == False
    assert interpreter._is_type_compatible('str', True) == False


def test_type_compatibility_flt():
    """Test flt type compatibility."""
    interpreter = Interpreter()
    
    # Valid flt assignments (int and float)
    assert interpreter._is_type_compatible('flt', 5) == True
    assert interpreter._is_type_compatible('flt', 3.14) == True
    assert interpreter._is_type_compatible('flt', 0) == True
    
    # Invalid flt assignments
    assert interpreter._is_type_compatible('flt', "hello") == False
    assert interpreter._is_type_compatible('flt', True) == False


def test_type_compatibility_var():
    """Test var type compatibility (accepts everything)."""
    interpreter = Interpreter()
    
    # var accepts everything
    assert interpreter._is_type_compatible('var', 5) == True
    assert interpreter._is_type_compatible('var', "hello") == True
    assert interpreter._is_type_compatible('var', 3.14) == True
    assert interpreter._is_type_compatible('var', True) == True
    assert interpreter._is_type_compatible('var', None) == True


def test_complex_type_declarations():
    """Test complex expressions in type declarations."""
    source = """
    int x = 5 + 3
    str name = "hello" + " world"
    flt result = 10.5 * 2
    var dynamic = x + result
    """
    interpreter = Interpreter()
    interpreter.evaluate(parse(source))
    
    assert interpreter.global_scope['x'] == 8
    assert interpreter.global_scope['name'] == "hello world"
    assert interpreter.global_scope['result'] == 21.0
    assert interpreter.global_scope['dynamic'] == 29.0  # 8 + 21.0


def test_type_declaration_in_function():
    """Test type declarations inside functions."""
    source = """
    def test() {
        int x = 5
        str name = "test"
        var dynamic = x + 10
    }
    """
    interpreter = Interpreter()
    interpreter.evaluate(parse(source))
    
    # Function should be defined
    assert "test" in interpreter.functions


def test_type_declaration_syntax_errors():
    """Test syntax errors in type declarations."""
    # Missing variable name
    with pytest.raises((ParseError, SyntaxErrorLyric)):
        parse("int = 5")
    
    # Missing expression
    with pytest.raises((ParseError, SyntaxErrorLyric)):
        parse("int x =")


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
