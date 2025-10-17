"""
Tests for declaration enforcement in Sprint 4 Task 2.
"""

import pytest
import sys
import os
import io
from contextlib import redirect_stdout

# Add the parent directory to the path so we can import lyric
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lyric_lang.parser import parse
from lyric_lang.interpreter import Interpreter
from lyric_lang.errors import RuntimeErrorLyric


class TestDeclarationEnforcement:
    """Test declaration enforcement for variables."""

    def test_undeclared_variable_assignment_error(self):
        """Test that assigning to undeclared variable throws an error."""
        source = '''
        def main() {
            x = 10
        }
        '''
        
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric, match="Variable 'x' used before declaration"):
            interpreter.interpret(program)

    def test_undeclared_variable_reference_error(self):
        """Test that referencing undeclared variable throws an error."""
        source = '''
        def main() {
            print(x)
        }
        '''
        
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric, match="Variable 'x' used before declaration"):
            interpreter.interpret(program)

    def test_declared_var_assignment_success(self):
        """Test that declared var variables can be assigned."""
        source = '''
        def main() {
            var x = 10
            print("x =", x)
        }
        '''
        
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        # This should work without error
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        output = f.getvalue().strip()
        assert output == "x = 10"

    def test_declared_static_type_assignment_success(self):
        """Test that declared static type variables can be assigned."""
        source = '''
        def main() {
            int x = 10
            print("x =", x)
        }
        '''
        
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        # This should work without error
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        output = f.getvalue().strip()
        assert output == "x = 10"

    def test_declared_var_reassignment_success(self):
        """Test that declared var variables can be reassigned."""
        source = '''
        def main() {
            var x = 10
            x = 20
            print("x =", x)
        }
        '''
        
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        # This should work without error
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        output = f.getvalue().strip()
        assert output == "x = 20"

    def test_declared_static_reassignment_success(self):
        """Test that declared static type variables can be reassigned."""
        source = '''
        def main() {
            int x = 10
            x = 20
            print("x =", x)
        }
        '''
        
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        # This should work without error
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        output = f.getvalue().strip()
        assert output == "x = 20"

    def test_multiple_undeclared_variables_error(self):
        """Test multiple undeclared variables throw appropriate errors."""
        source = '''
        def main() {
            x = 10
            y = 20
        }
        '''
        
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric, match="Variable 'x' used before declaration"):
            interpreter.interpret(program)

    def test_mixed_declared_undeclared_error(self):
        """Test mixed declared and undeclared variables."""
        source = '''
        def main() {
            var x = 10
            y = 20  # This should fail
        }
        '''
        
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric, match="Variable 'y' used before declaration"):
            interpreter.interpret(program)

    def test_function_parameter_declaration_success(self):
        """Test that function parameters are considered declared."""
        source = '''
        def test_func(param) {
            print("param =", param)
        }
        
        def main() {
            test_func(42)
        }
        '''
        
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        # This should work without error
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        output = f.getvalue().strip()
        assert output == "param = 42"

    def test_nested_scope_declaration_enforcement(self):
        """Test declaration enforcement in nested scopes."""
        source = '''
        def outer_func() {
            var x = 10
            print("outer x =", x)
            
            # This should fail - y is not declared
            y = 20
        }
        
        def main() {
            outer_func()
        }
        '''
        
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric, match="Variable 'y' used before declaration"):
            interpreter.interpret(program)

    def test_class_attribute_declaration_success(self):
        """Test that class attributes are considered declared."""
        source = '''
        class TestClass:
        def init(self) {
            self.attr = 42
        }
        +++
        
        def main() {
            var obj = TestClass()
            print("obj created successfully")
        }
        '''
        
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        # This should work without error
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        output = f.getvalue().strip()
        assert output == "obj created successfully"

    def test_error_message_format_undeclared_assignment(self):
        """Test that error message format is correct for undeclared assignment."""
        source = '''
        def main() {
            x = 10
        }
        '''
        
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        try:
            interpreter.interpret(program)
            assert False, "Should have raised an error"
        except RuntimeErrorLyric as e:
            assert "Variable 'x' used before declaration" in str(e)

    def test_error_message_format_undeclared_reference(self):
        """Test that error message format is correct for undeclared reference."""
        source = '''
        def main() {
            print(x)
        }
        '''
        
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        try:
            interpreter.interpret(program)
            assert False, "Should have raised an error"
        except RuntimeErrorLyric as e:
            assert "Variable 'x' used before declaration" in str(e)

    def test_complex_declaration_scenario(self):
        """Test complex scenario with multiple declarations and assignments."""
        source = '''
        def main() {
            var dynamic_var = 10
            int static_var = 20
            str name_var = "test"
            
            print("dynamic_var =", dynamic_var)
            print("static_var =", static_var)
            print("name_var =", name_var)
            
            # Reassignments should work
            dynamic_var = "changed"
            static_var = 30
            name_var = "updated"
            
            print("after changes:")
            print("dynamic_var =", dynamic_var)
            print("static_var =", static_var)
            print("name_var =", name_var)
        }
        '''
        
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        # This should work without error
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        output = f.getvalue().strip()
        expected = ("dynamic_var = 10\nstatic_var = 20\nname_var = test\n"
                   "after changes:\ndynamic_var = changed\nstatic_var = 30\nname_var = updated")
        assert output == expected
