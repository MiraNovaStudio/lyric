"""
Tests for type_tests.ly - Type System functionality.
"""

import pytest
import sys
import os
import io
from contextlib import redirect_stdout

# Add the parent directory to the path so we can import lyric
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lyric.parser import parse
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric


class TestTypeTests:
    """Test type system functionality from type_tests.ly."""

    def capture_output(self, source: str) -> str:
        """Capture output from running Lyric source code."""
        program = parse(source)
        interpreter = Interpreter()
        
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        return f.getvalue().strip()

    def test_type_tests_execution(self):
        """Test that type_tests.ly runs successfully through CLI."""
        source = '''
        # Basic type declarations
        int age = 25
        float pi = 3.14159
        str name = "Aeonath"
        bool is_active = true
        None null_value = None
        
        # Type inference
        auto_int = 42
        auto_float = 2.718
        auto_string = "inferred"
        auto_bool = false
        auto_none = None
        
        def int add_numbers(int a, int b) {
            return a + b
        }
        
        def str format_greeting(str name, int age) {
            return "Hello " + name + ", you are " + str(age) + " years old"
        }
        
        def bool is_even(int number) {
            if number % 2 == 0:
                return true
            else:
                return false
            end
        }
        
        def None do_nothing() {
            print("Doing nothing...")
        }
        
        def main() {
            print("=== Type System Tests ===")
            
            # Test basic type declarations
            print("1. Basic type declarations:")
            print("age:", age, "type:", type(age))
            print("pi:", pi, "type:", type(pi))
            print("name:", name, "type:", type(name))
            print("is_active:", is_active, "type:", type(is_active))
            print("null_value:", null_value, "type:", type(null_value))
            
            # Test type inference
            print("\\n2. Type inference:")
            print("auto_int:", auto_int, "type:", type(auto_int))
            print("auto_float:", auto_float, "type:", type(auto_float))
            print("auto_string:", auto_string, "type:", type(auto_string))
            print("auto_bool:", auto_bool, "type:", type(auto_bool))
            print("auto_none:", auto_none, "type:", type(auto_none))
            
            # Test function calls with correct types
            print("\\n3. Function calls with correct types:")
            result1 = add_numbers(10, 20)
            print("add_numbers(10, 20) =", result1)
            
            greeting = format_greeting("Alice", 30)
            print("format_greeting result:", greeting)
            
            even_check = is_even(16)
            print("is_even(16) =", even_check)
            
            do_nothing()
            
            print("\\n=== Type System Tests Complete ===")
        }
        '''
        
        output = self.capture_output(source)
        
        # Verify key outputs
        assert "=== Type System Tests ===" in output
        assert "age: 25 type: int" in output
        assert "pi: 3.14159 type: float" in output
        assert "name: Aeonath type: str" in output
        assert "is_active: True type: bool" in output
        assert "null_value: None type: None" in output
        
        assert "auto_int: 42 type: int" in output
        assert "auto_float: 2.718 type: float" in output
        assert "auto_string: inferred type: str" in output
        assert "auto_bool: False type: bool" in output
        assert "auto_none: None type: None" in output
        
        assert "add_numbers(10, 20) = 30" in output
        assert "Hello Alice, you are 30 years old" in output
        assert "is_even(16) = True" in output
        assert "Doing nothing..." in output
        assert "=== Type System Tests Complete ===" in output

    def test_type_enforcement_errors(self):
        """Test that type enforcement raises appropriate errors."""
        # Test function parameter type error
        source = '''
        def int strict_add(int x, int y) {
            return x + y
        }
        
        def main() {
            # This should cause a type error
            result = strict_add("hello", "world")
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for parameter 'x': expected int, got str" in error_msg

    def test_variable_type_enforcement(self):
        """Test that variable type enforcement works."""
        source = '''
        def main() {
            int x = 42
            # This should cause a type error
            x = "wrong type"
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'x': expected int, got str" in error_msg

    def test_none_type_enforcement(self):
        """Test None type enforcement."""
        source = '''
        def main() {
            None x = None
            # This should cause a type error
            x = "wrong type"
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'x': expected None, got str" in error_msg

