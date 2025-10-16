"""
Tests for Task 6 - Runtime Safety and Error Messages
"""

import pytest
import io
import sys
from lyric.parser import parse
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric


class TestRuntimeSafetyAndErrorMessages:
    """Test runtime safety and enhanced error messages."""

    def test_enhanced_type_error_messages(self):
        """Test A17: Errors show enhanced context and descriptive messages."""
        source = '''
def int add_numbers(int a, int b) {
    return a + b
}

def main() {
    result = add_numbers(5, "hello")
}
'''
        
        program = parse(source, 'test_file.ly')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        # Check for enhanced error context
        assert "In function 'add_numbers'" in error_msg
        assert "Type mismatch for parameter 'b'" in error_msg
        assert "expected int, got str" in error_msg
        assert "Called with argument 2 (b) = 'hello'" in error_msg

    def test_function_call_type_errors(self):
        """Test A18: Calling a function with incorrect argument types raises a descriptive error."""
        source = '''
def str process_data(str name, int age, bool active) {
    return "Processing: " + name
}

def main() {
    result = process_data(123, "twenty", None)
}
'''
        
        program = parse(source, 'type_test.ly')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "In function 'process_data'" in error_msg
        assert "Type mismatch for parameter 'name'" in error_msg
        assert "expected str, got int" in error_msg
        assert "Called with argument 1 (name) = 123" in error_msg

    def test_return_type_error_messages(self):
        """Test enhanced return type error messages."""
        source = '''
def str get_string() {
    return 42
}

def main() {
    result = get_string()
}
'''
        
        program = parse(source, 'return_test.ly')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Function 'get_string' return type mismatch" in error_msg
        assert "expected str, got int" in error_msg
        assert "returned value: 42" in error_msg

    def test_list_indexing_error_messages(self):
        """Test enhanced list indexing error messages."""
        source = '''
def main() {
    numbers = [1, 2, 3]
    # Test invalid index type
    result1 = numbers["invalid"]
    # Test out of range index
    result2 = numbers[10]
}
'''
        
        program = parse(source, 'index_test.ly')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "List indexing error" in error_msg
        assert "index must be an integer, got str" in error_msg
        assert "value: 'invalid'" in error_msg

    def test_list_index_out_of_range_message(self):
        """Test enhanced list index out of range message."""
        source = '''
def main() {
    numbers = [1, 2, 3]
    result = numbers[5]
}
'''
        
        program = parse(source, 'range_test.ly')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "List index 5 out of range" in error_msg
        assert "list has 3 elements" in error_msg
        assert "valid indices: 0 to 2" in error_msg

    def test_dictionary_key_error_messages(self):
        """Test enhanced dictionary key error messages."""
        source = '''
def main() {
    person = {"name": "Alice", "age": 30}
    result = person["height"]
}
'''
        
        program = parse(source, 'dict_test.ly')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Dictionary key 'height' not found" in error_msg
        assert "available keys: ['name', 'age']" in error_msg

    def test_string_indexing_error_messages(self):
        """Test enhanced string indexing error messages."""
        source = '''
def main() {
    text = "hello"
    # Test invalid index type
    result1 = text["invalid"]
    # Test out of range index
    result2 = text[10]
}
'''
        
        program = parse(source, 'string_test.ly')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "String indexing error" in error_msg
        assert "index must be an integer, got str" in error_msg

    def test_arithmetic_error_messages(self):
        """Test enhanced arithmetic error messages."""
        source = '''
def main() {
    result = 10 / 0
}
'''
        
        program = parse(source, 'arithmetic_test.ly')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Arithmetic error: division by zero" in error_msg

    def test_builtin_function_error_messages(self):
        """Test enhanced built-in function error messages."""
        source = '''
def main() {
    result = int("hello", "world")
}
'''
        
        program = parse(source, 'builtin_test.ly')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Function 'int()' argument error" in error_msg
        assert "takes 1 argument(s), got 2" in error_msg
        assert "arguments: [\"'hello'\", \"'world'\"]" in error_msg

    def test_type_conversion_error_messages(self):
        """Test enhanced type conversion error messages."""
        source = '''
def main() {
    result = int("not_a_number")
}
'''
        
        program = parse(source, 'conversion_test.ly')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type conversion error: int() failed for value 'not_a_number'" in error_msg

    def test_no_python_stack_traces(self):
        """Test A19: No Python stack traces appear in user-facing output."""
        source = '''
def main() {
    undefined_variable
}
'''
        
        program = parse(source, 'undefined_test.ly')
        interpreter = Interpreter()
        
        # Capture stderr to check for Python stack traces
        old_stderr = sys.stderr
        stderr_capture = io.StringIO()
        sys.stderr = stderr_capture
        
        try:
            with pytest.raises(RuntimeErrorLyric):
                interpreter.interpret(program)
        finally:
            sys.stderr = old_stderr
        
        # Check that no Python traceback appears in stderr
        stderr_output = stderr_capture.getvalue()
        assert "Traceback (most recent call last):" not in stderr_output
        assert "File \"" not in stderr_output

    def test_indexing_non_indexable_object(self):
        """Test error message for indexing non-indexable objects."""
        source = '''
def main() {
    number = 42
    result = number[0]
}
'''
        
        program = parse(source, 'non_indexable_test.ly')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Cannot index object of type int" in error_msg
        assert "only lists, dictionaries, and strings support indexing" in error_msg

    def test_consistent_error_categories(self):
        """Test that error categories are consistent and descriptive."""
        # Test multiple error types to ensure consistent categorization
        test_cases = [
            ('arithmetic_error.ly', 'result = 10 / 0', 'Arithmetic error'),
            ('type_error.ly', 'numbers = [1, 2, 3]\n    result = numbers["invalid"]', 'List indexing error'),
            ('key_error.ly', 'person = {"name": "Alice"}\n    result = person["age"]', 'Dictionary key'),
            ('conversion_error.ly', 'result = int("invalid")', 'Type conversion error'),
            ('function_error.ly', 'result = int("a", "b")', 'Function \'int()\' argument error')
        ]
        
        for filename, code, expected_category in test_cases:
            source = f'''
def main() {{
    {code}
}}
'''
            program = parse(source, filename)
            interpreter = Interpreter()
            
            with pytest.raises(RuntimeErrorLyric) as exc_info:
                interpreter.interpret(program)
            
            error_msg = str(exc_info.value)
            assert expected_category in error_msg
