"""
Tests for the 'var' keyword functionality in Sprint 4 Task 1.
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


class TestVarKeyword:
    """Test the 'var' keyword for dynamic typing."""

    def capture_output(self, source: str) -> str:
        """Capture output from running Lyric source code."""
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        return f.getvalue().strip()

    def test_var_declaration_basic(self):
        """Test basic var declaration: var x = 10"""
        source = '''
        def main() {
            var x = 10
            print("x =", x)
        }
        '''
        
        output = self.capture_output(source)
        assert output == "x = 10"

    def test_var_type_reassignment(self):
        """Test that var variables can change type at runtime."""
        source = '''
        def main() {
            var x = 10
            print("x =", x, "type:", type(x))
            
            x = "hello"
            print("x =", x, "type:", type(x))
            
            x = true
            print("x =", x, "type:", type(x))
            
            x = [1, 2, 3]
            print("x =", x, "type:", type(x))
        }
        '''
        
        output = self.capture_output(source)
        expected = "x = 10 type: int\nx = hello type: str\nx = True type: bool\nx = [1, 2, 3] type: list"
        assert output == expected

    def test_var_with_different_initial_types(self):
        """Test var declarations with different initial types."""
        source = '''
        def main() {
            var str_var = "hello"
            var int_var = 42
            var bool_var = true
            var list_var = [1, 2, 3]
            var dict_var = {"key": "value"}
            
            print("str_var:", str_var, type(str_var))
            print("int_var:", int_var, type(int_var))
            print("bool_var:", bool_var, type(bool_var))
            print("list_var:", list_var, type(list_var))
            print("dict_var:", dict_var, type(dict_var))
        }
        '''
        
        output = self.capture_output(source)
        expected = "str_var: hello str\nint_var: 42 int\nbool_var: True bool\nlist_var: [1, 2, 3] list\ndict_var: {key: \"value\"} dict"
        assert output == expected

    def test_var_vs_static_typing(self):
        """Test var variables vs statically typed variables."""
        source = '''
        def main() {
            var dynamic_var = 10
            int static_var = 20
            
            print("dynamic_var:", dynamic_var)
            print("static_var:", static_var)
            
            # Var can change type
            dynamic_var = "changed to string"
            print("dynamic_var after change:", dynamic_var)
            
            # Static should maintain type (this should work)
            static_var = 30
            print("static_var after reassignment:", static_var)
        }
        '''
        
        output = self.capture_output(source)
        expected = "dynamic_var: 10\nstatic_var: 20\ndynamic_var after change: changed to string\nstatic_var after reassignment: 30"
        assert output == expected

    def test_var_with_functions(self):
        """Test var variables in function context."""
        source = '''
        def test_function() {
            var local_var = 100
            print("local_var in function:", local_var)
            
            local_var = "changed in function"
            print("local_var changed:", local_var)
            
            return local_var
        }
        
        def main() {
            var global_var = "global"
            print("global_var before function:", global_var)
            
            var result = test_function()
            print("function returned:", result)
            
            global_var = 999
            print("global_var after change:", global_var)
        }
        '''
        
        output = self.capture_output(source)
        expected = "global_var before function: global\nlocal_var in function: 100\nlocal_var changed: changed in function\nfunction returned: changed in function\nglobal_var after change: 999"
        assert output == expected

    def test_var_with_arithmetic_operations(self):
        """Test var variables with arithmetic operations."""
        source = '''
        def main() {
            var x = 10
            var y = 20
            
            print("x + y =", x + y)
            
            x = 3.14
            y = 2.0
            print("x * y =", x * y)
            
            x = "hello"
            y = " world"
            print("x + y =", x + y)
        }
        '''
        
        output = self.capture_output(source)
        expected = "x + y = 30\nx * y = 6.28\nx + y = hello world"
        assert output == expected

    def test_var_undeclared_assignment_error(self):
        """Test that undeclared variables throw errors (Task 2 implementation)."""
        source = '''
        def main() {
            # This should cause an error with Task 2 declaration enforcement
            x = 10
            print("x =", x)
        }
        '''
        
        # Task 2 now enforces declarations - this should throw an error
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric, match="Variable 'x' used before declaration"):
            interpreter.interpret(program)

    def test_var_with_complex_expressions(self):
        """Test var variables with complex expressions."""
        source = '''
        def main() {
            var result = 0
            
            # Start with number
            result = 5 + 3 * 2
            print("numeric result:", result)
            
            # Change to boolean
            result = true and false
            print("boolean result:", result)
            
            # Change to string
            result = "complex" + " " + "expression"
            print("string result:", result)
            
            # Change to list
            result = [1, 2, 3] + [4, 5]
            print("list result:", result)
        }
        '''
        
        output = self.capture_output(source)
        expected = "numeric result: 11\nboolean result: False\nstring result: complex expression\nlist result: [1, 2, 3, 4, 5]"
        assert output == expected

    def test_var_parsing_errors(self):
        """Test that var parsing handles errors correctly."""
        # Test missing variable name
        source1 = '''
        def main() {
            var = 10
        }
        '''
        
        with pytest.raises(Exception):  # Should be a parse error
            self.capture_output(source1)
        
        # Test missing assignment
        source2 = '''
        def main() {
            var x
        }
        '''
        
        with pytest.raises(Exception):  # Should be a parse error
            self.capture_output(source2)

    def test_var_multiple_declarations(self):
        """Test multiple var declarations in the same scope."""
        source = '''
        def main() {
            var x = 10
            var y = "hello"
            var z = true
            
            print("x:", x, "y:", y, "z:", z)
            
            # Change all types
            x = "changed"
            y = 42
            z = [1, 2, 3]
            
            print("after changes - x:", x, "y:", y, "z:", z)
        }
        '''
        
        output = self.capture_output(source)
        expected = "x: 10 y: hello z: True\nafter changes - x: changed y: 42 z: [1, 2, 3]"
        assert output == expected
