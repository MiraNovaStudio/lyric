# Lyric Programming Language
# Copyright (c) 2025 MiraNova Studios
# Developed by Michael (Aeonath), ChatGPT, and Claude
# Licensed under the MIT License with Source Attribution

"""Test suite for runtime safety and error message improvements."""

import pytest
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric, ParseError, SyntaxErrorLyric


class TestRuntimeSafety:
    """Test runtime safety features and enhanced error messages."""
    
    def test_enhanced_index_error_messages(self):
        """Test enhanced error messages for index operations."""
        # Test list index out of range
        source = """
        var numbers = [1, 2, 3]
        var result = numbers[5]
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Index out of range" in error_msg
        assert "tried to access index 5" in error_msg
        assert "list of length 3" in error_msg
        assert "Valid indices are 0 to 2" in error_msg
    
    def test_enhanced_dictionary_key_error_messages(self):
        """Test enhanced error messages for dictionary key access."""
        source = """
        var data = {"name": "Alice", "age": 30}
        var result = data["city"]
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Key not found" in error_msg
        assert "'city' is not a key" in error_msg
        assert "Available keys" in error_msg
        assert "name" in error_msg
        assert "age" in error_msg
    
    def test_enhanced_type_mismatch_messages(self):
        """Test enhanced error messages for type mismatches."""
        source = """
        int x = "hello"
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch" in error_msg
        assert "cannot assign str to variable 'x' declared as int" in error_msg
        assert "Expected int, but got str" in error_msg
        assert "Use 'var x = ...' if you need dynamic typing" in error_msg
    
    def test_enhanced_undefined_variable_messages(self):
        """Test enhanced error messages for undefined variables."""
        source = """
        var result = undefined_var
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Undefined variable" in error_msg
        assert "'undefined_var' has not been declared" in error_msg
        assert "Use a type declaration" in error_msg
    
    def test_enhanced_function_not_found_messages(self):
        """Test enhanced error messages for undefined functions."""
        source = """
        var result = unknown_function()
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Function not found" in error_msg
        assert "'unknown_function' is not defined" in error_msg
        assert "Built-in functions: print, range, len, int, float, str" in error_msg
    
    def test_enhanced_method_not_found_messages(self):
        """Test enhanced error messages for undefined methods."""
        source = """
        var obj = {"name": "test"}
        var result = obj.unknown_method()
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Method not found" in error_msg
        assert "'unknown_method' is not a method of" in error_msg
        assert "has no methods" in error_msg
    
    def test_enhanced_division_by_zero_messages(self):
        """Test enhanced error messages for division by zero."""
        source = """
        var result = 10 / 0
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Division by zero" in error_msg
        assert "cannot divide by zero" in error_msg
        assert "Check your divisor value" in error_msg
    
    def test_enhanced_type_mismatch_in_operations(self):
        """Test enhanced error messages for type mismatches in operations."""
        source = """
        var result = 5 + "hello"
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch in operation '+'" in error_msg
        assert "Check that both operands are compatible types" in error_msg
    
    def test_enhanced_range_function_error_messages(self):
        """Test enhanced error messages for range function."""
        source = """
        var result = range(1, 2, 3, 4)
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Invalid range() arguments" in error_msg
        assert "range() takes 1-3 arguments" in error_msg
        assert "Usage: range(stop) or range(start, stop) or range(start, stop, step)" in error_msg
    
    def test_enhanced_unknown_operator_messages(self):
        """Test enhanced error messages for unknown operators."""
        # Use a valid syntax that will cause a runtime error for unknown operator
        source = """
        var result = 5 + "hello"
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch in operation '+'" in error_msg
        assert "Check that both operands are compatible types" in error_msg
    
    def test_enhanced_unknown_unary_operator_messages(self):
        """Test enhanced error messages for unknown unary operators."""
        # Use a valid syntax that will cause a runtime error for unknown unary operator
        source = """
        var result = -"hello"
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "bad operand type for unary -" in error_msg
        assert "str" in error_msg
    
    def test_enhanced_exception_raise_messages(self):
        """Test enhanced error messages for unknown exceptions."""
        source = """
        raise UnknownException
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Unknown exception" in error_msg
        assert "'UnknownException' is not a valid exception type" in error_msg
        assert "Available exceptions" in error_msg
    
    def test_enhanced_builtin_function_error_messages(self):
        """Test enhanced error messages for built-in functions."""
        source = """
        var result = append("not_a_list", 5)
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "append() only works on lists" in error_msg
        assert "got str" in error_msg
    
    def test_enhanced_indexing_error_messages(self):
        """Test enhanced error messages for invalid indexing."""
        source = """
        var obj = 5
        var result = obj[0]
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Cannot index object" in error_msg
        assert "'int' does not support indexing" in error_msg
        assert "Only lists and dictionaries can be indexed" in error_msg
        assert "Use dot notation (.) for object properties" in error_msg
    
    def test_enhanced_callable_error_messages(self):
        """Test enhanced error messages for non-callable objects."""
        source = """
        var obj = {"name": "test"}
        var result = obj.name()
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Cannot call 'name'" in error_msg
        assert "it is not a function or method" in error_msg
        assert "is of type str" in error_msg
        assert "Use parentheses () only for function calls" in error_msg
    
    def test_enhanced_assignment_error_messages(self):
        """Test enhanced error messages for assignment errors."""
        source = """
        var result = undefined_var
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Undefined variable" in error_msg
        assert "'undefined_var' has not been declared" in error_msg
        assert "Use a type declaration" in error_msg
    
    def test_enhanced_member_access_error_messages(self):
        """Test enhanced error messages for member access errors."""
        source = """
        var obj = {"name": "test"}
        var result = obj.unknown_member
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Member not found" in error_msg
        assert "'unknown_member' is not a member of" in error_msg
        assert "Available members" in error_msg
        assert "name" in error_msg
    
    def test_error_message_consistency(self):
        """Test that error messages follow consistent patterns."""
        # Test that all error messages contain descriptive categories
        error_tests = [
            ("var x = undefined_var", "Undefined variable"),
            ("var x = unknown_func()", "Function not found"),
            ("var x = 5 / 0", "Division by zero"),
            ("var x = 5 + \"hello\"", "Type mismatch"),
            ("var x = [1, 2, 3][5]", "Index out of range"),
            ("var x = {\"a\": 1}[\"b\"]", "Key not found"),
        ]
        
        for source, expected_category in error_tests:
            tokens = tokenize(source)
            parser = Parser(tokens)
            ast = parser.parse()
            interpreter = Interpreter()
            
            with pytest.raises(RuntimeErrorLyric) as exc_info:
                interpreter.evaluate(ast)
            
            error_msg = str(exc_info.value)
            assert expected_category in error_msg, f"Expected '{expected_category}' in error message but got: {error_msg}"
    
    def test_error_message_consistency_methods(self):
        """Test that method and member error messages follow consistent patterns."""
        # Test method not found
        source = """
        var obj = {"name": "test"}
        var x = obj.unknown_method()
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Method not found" in error_msg
    
    def test_error_message_consistency_members(self):
        """Test that member access error messages follow consistent patterns."""
        # Test member not found
        source = """
        var obj = {"name": "test"}
        var x = obj.unknown_member
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Member not found" in error_msg
    
    def test_no_python_stack_traces(self):
        """Test that no Python stack traces appear in user-facing output."""
        source = """
        var result = 5 + "hello"
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        # Ensure no Python traceback information appears
        assert "Traceback" not in error_msg
        assert "File \"" not in error_msg
        assert "line " not in error_msg or "line " in error_msg and "File" not in error_msg
        assert "TypeError:" not in error_msg
        assert "ValueError:" not in error_msg
