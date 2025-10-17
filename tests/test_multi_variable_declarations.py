"""
Tests for multi-variable declarations in Sprint 4 Task 3.
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


class TestMultiVariableDeclarations:
    """Test multi-variable declarations functionality."""

    def capture_output(self, source: str) -> str:
        """Capture output from running Lyric source code."""
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        return f.getvalue().strip()

    def test_var_multi_declaration_basic(self):
        """Test basic multi-variable declaration with var."""
        source = '''
        def main() {
            var x, y, z
            
            x = 10
            y = "hello"
            z = true
            
            print("x =", x)
            print("y =", y)
            print("z =", z)
        }
        '''
        
        output = self.capture_output(source)
        expected = "x = 10\ny = hello\nz = True"
        assert output == expected

    def test_static_type_multi_declaration(self):
        """Test multi-variable declaration with static types."""
        source = '''
        def main() {
            int a, b, c
            
            a = 5
            b = 10
            c = 15
            
            print("a =", a)
            print("b =", b)
            print("c =", c)
        }
        '''
        
        output = self.capture_output(source)
        expected = "a = 5\nb = 10\nc = 15"
        assert output == expected

    def test_mixed_type_multi_declaration(self):
        """Test multi-variable declaration with mixed types."""
        source = '''
        def main() {
            var x, int y, str z, bool flag
            
            x = 3.14
            y = 42
            z = "mixed"
            flag = false
            
            print("x =", x, type(x))
            print("y =", y, type(y))
            print("z =", z, type(z))
            print("flag =", flag, type(flag))
        }
        '''
        
        output = self.capture_output(source)
        expected = "x = 3.14 float\ny = 42 int\nz = mixed str\nflag = False bool"
        assert output == expected

    def test_multi_declaration_with_same_type(self):
        """Test multiple variables of the same type."""
        source = '''
        def main() {
            str name, str surname, str middle
            
            name = "John"
            surname = "Doe"
            middle = "Michael"
            
            print("Full name:", name, middle, surname)
        }
        '''
        
        output = self.capture_output(source)
        assert output == "Full name: John Michael Doe"

    def test_uninitialized_variable_error(self):
        """Test that uninitialized multi-declared variables throw errors."""
        source = '''
        def main() {
            var x, y, z
            
            print(x)  # This should cause an error
        }
        '''
        
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric, match="Variable 'x' referenced before assignment"):
            interpreter.interpret(program)

    def test_multi_declaration_reassignment(self):
        """Test reassignment of multi-declared variables."""
        source = '''
        def main() {
            var x, y, z
            
            x = 10
            y = "hello"
            z = true
            
            # Reassign with different types
            x = "changed"
            y = 42
            z = [1, 2, 3]
            
            print("x =", x, type(x))
            print("y =", y, type(y))
            print("z =", z, type(z))
        }
        '''
        
        output = self.capture_output(source)
        expected = "x = changed str\ny = 42 int\nz = [1, 2, 3] list"
        assert output == expected

    def test_complex_multi_declaration_scenario(self):
        """Test complex scenario with multiple multi-declarations."""
        source = '''
        def main() {
            var a, b, c
            int x, y, z
            str name, str city
            
            a = 10
            b = 20
            c = 30
            x = 100
            y = 200
            z = 300
            name = "Alice"
            city = "New York"
            
            print("vars:", a, b, c)
            print("ints:", x, y, z)
            print("strings:", name, city)
        }
        '''
        
        output = self.capture_output(source)
        expected = "vars: 10 20 30\nints: 100 200 300\nstrings: Alice New York"
        assert output == expected

    def test_multi_declaration_with_none_type(self):
        """Test multi-declaration with None type."""
        source = '''
        def main() {
            None ptr1, None ptr2, None ptr3
            
            ptr1 = None
            ptr2 = None
            ptr3 = None
            
            print("ptr1 =", ptr1)
            print("ptr2 =", ptr2)
            print("ptr3 =", ptr3)
        }
        '''
        
        output = self.capture_output(source)
        expected = "ptr1 = None\nptr2 = None\nptr3 = None"
        assert output == expected

    def test_multi_declaration_in_function(self):
        """Test multi-declarations in function scope."""
        source = '''
        def test_function() {
            var local1, local2, local3
            
            local1 = 100
            local2 = "local"
            local3 = true
            
            return local1 + len(local2)
        }
        
        def main() {
            var result = test_function()
            print("result =", result)
        }
        '''
        
        output = self.capture_output(source)
        assert output == "result = 105"

    def test_multi_declaration_with_float_type(self):
        """Test multi-declaration with float type."""
        source = '''
        def main() {
            float pi, float e, float phi
            
            pi = 3.14159
            e = 2.71828
            phi = 1.61803
            
            print("pi =", pi)
            print("e =", e)
            print("phi =", phi)
        }
        '''
        
        output = self.capture_output(source)
        expected = "pi = 3.14159\ne = 2.71828\nphi = 1.61803"
        assert output == expected

    def test_multi_declaration_parsing_error(self):
        """Test that malformed multi-declarations throw parse errors."""
        # Missing variable name after comma
        source1 = '''
        def main() {
            var x, , z
        }
        '''
        
        with pytest.raises(Exception):  # Should be a parse error
            parse(source1, 'test')
        
        # Missing type after comma
        source2 = '''
        def main() {
            int x, , z
        }
        '''
        
        with pytest.raises(Exception):  # Should be a parse error
            parse(source2, 'test')

    def test_multi_declaration_with_bool_type(self):
        """Test multi-declaration with bool type."""
        source = '''
        def main() {
            bool flag1, bool flag2, bool flag3
            
            flag1 = true
            flag2 = false
            flag3 = true
            
            print("flags:", flag1, flag2, flag3)
        }
        '''
        
        output = self.capture_output(source)
        assert output == "flags: True False True"

    def test_multi_declaration_type_enforcement(self):
        """Test that type enforcement works with multi-declarations."""
        source = '''
        def main() {
            int x, int y, int z
            
            x = 10  # OK
            y = 20  # OK
            z = "hello"  # This should cause a type error
        }
        '''
        
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric, match="Type mismatch for variable 'z': expected int, got str"):
            interpreter.interpret(program)

    def test_multi_declaration_vs_single_declaration(self):
        """Test that multi-declarations work alongside single declarations."""
        source = '''
        def main() {
            var x, y, z  # Multi-declaration
            int single_var = 42  # Single declaration
            
            x = 10
            y = "hello"
            z = true
            
            print("multi:", x, y, z)
            print("single:", single_var)
        }
        '''
        
        output = self.capture_output(source)
        expected = "multi: 10 hello True\nsingle: 42"
        assert output == expected
