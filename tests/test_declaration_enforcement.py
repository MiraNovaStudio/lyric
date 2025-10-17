"""
Test suite for strict variable declaration enforcement in Lyric.
This implements the SUPERNOVA remediation plan for declaration enforcement.
"""

import pytest
from lyric_lang.parser import parse
from lyric_lang.interpreter import interpret
from lyric_lang.errors import RuntimeErrorLyric


class TestDeclarationEnforcement:
    """Test strict variable declaration enforcement."""

    def test_valid_declaration_with_assignment(self):
        """Test valid variable declaration with immediate assignment."""
        code = """
        int x = 10
        print(x)
        """
        
        program = parse(code)
        interpret(program)
        
        # Should execute without errors (if we get here, no exception was raised)
        assert True

    def test_valid_declaration_without_assignment(self):
        """Test valid variable declaration without assignment."""
        code = """
        int x
        x = 10
        print(x)
        """
        
        program = parse(code)
        interpret(program)
        
        # Should execute without errors (if we get here, no exception was raised)
        assert True

    def test_assignment_to_undeclared_variable_raises_error(self):
        """Test that assignment to undeclared variable raises error."""
        code = """
        x = 10
        """
        
        program = parse(code)
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpret(program)
        
        assert "Variable 'x' used before declaration" in str(exc_info.value)

    def test_type_mismatch_raises_error(self):
        """Test that type mismatch raises error."""
        code = """
        int x = 10
        x = "hello"
        """
        
        program = parse(code)
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpret(program)
        
        assert "Type mismatch for variable 'x'" in str(exc_info.value)
        assert "expected int, got str" in str(exc_info.value)

    def test_var_keyword_allows_any_type(self):
        """Test that var keyword allows any type assignment."""
        code = """
        var x = 10
        print(x)
        x = "hello"
        print(x)
        x = true
        print(x)
        """
        
        program = parse(code)
        interpret(program)
        
        # Should execute without errors (if we get here, no exception was raised)
        assert True

    def test_var_declaration_without_assignment(self):
        """Test var declaration without assignment."""
        code = """
        var x
        x = 10
        print(x)
        """
        
        program = parse(code)
        interpret(program)
        
        # Should execute without errors (if we get here, no exception was raised)
        assert True

    def test_multiple_type_declarations(self):
        """Test multiple type declarations."""
        code = """
        int x = 10
        str name = "Aeonath"
        bool is_active = true
        var count = 5
        print(x)
        print(name)
        print(is_active)
        print(count)
        """
        
        program = parse(code)
        interpret(program)
        
        # Should execute without errors (if we get here, no exception was raised)
        assert True

    def test_redeclaration_raises_error(self):
        """Test that redeclaring a variable raises error."""
        code = """
        int x = 10
        int x = 20
        """
        
        program = parse(code)
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpret(program)
        
        assert "Variable 'x' already declared in this scope" in str(exc_info.value)

    def test_assignment_to_declared_variable_works(self):
        """Test assignment to already declared variable works."""
        code = """
        int x = 10
        print(x)
        x = 20
        print(x)
        """
        
        program = parse(code)
        interpret(program)
        
        # Should execute without errors (if we get here, no exception was raised)
        assert True

    def test_scope_isolation(self):
        """Test that variables are properly scoped."""
        code = """
        int x = 10
        def test_func():
            int x = 20
            print(x)
        test_func()
        print(x)
        """
        
        program = parse(code)
        interpret(program)
        
        # Should execute without errors (if we get here, no exception was raised)
        assert True

    def test_all_supported_types(self):
        """Test all supported type declarations."""
        code = """
        int i = 42
        float f = 3.14
        str s = "hello"
        bool b = true
        list l = [1, 2, 3]
        dict d = {"key": "value"}
        var v = "anything"
        
        print(i)
        print(f)
        print(s)
        print(b)
        print(l)
        print(d)
        print(v)
        """
        
        program = parse(code)
        interpret(program)
        
        # Should execute without errors (if we get here, no exception was raised)
        assert True

    def test_function_parameters_with_types(self):
        """Test function parameters with type declarations."""
        code = """
        def add(int a, int b):
            return a + b
        
        int result = add(5, 3)
        print(result)
        """
        
        program = parse(code)
        interpret(program)
        
        # Should execute without errors (if we get here, no exception was raised)
        assert True

    def test_conditional_declarations(self):
        """Test declarations within conditional blocks."""
        code = """
        bool condition = true
        if condition:
            int x = 10
            print(x)
        else:
            str x = "hello"
            print(x)
        """
        
        program = parse(code)
        interpret(program)
        
        # Should execute without errors (if we get here, no exception was raised)
        assert True

    def test_loop_declarations(self):
        """Test declarations within loop blocks."""
        code = """
        given i in range(3):
            int count = i * 2
            print(count)
        done
        """
        
        program = parse(code)
        interpret(program)
        
        # Should execute without errors (if we get here, no exception was raised)
        assert True

    def test_class_attribute_declarations(self):
        """Test class attribute declarations."""
        code = """
        class Person:
            str name
            int age
            
            def __init__(self, str n, int a):
                self.name = n
                self.age = a
        
        Person p = Person("Alice", 25)
        print(p.name)
        print(p.age)
        """
        
        program = parse(code)
        interpret(program)
        
        # Should execute without errors (if we get here, no exception was raised)
        assert True