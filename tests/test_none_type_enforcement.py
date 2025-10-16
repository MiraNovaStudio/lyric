"""
Tests for None type enforcement in Lyric.
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import lyric
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lyric.parser import parse
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric


class TestNoneTypeEnforcement:
    """Test None type enforcement for variable assignments."""

    def test_none_variable_declaration_and_assignment(self):
        """Test declaring a None variable and assigning None to it."""
        source = '''
        def main() {
            None x = None
            print("x is None:", x)
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        # Capture output
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        output = f.getvalue().strip()
        assert "x is None: None" in output

    def test_none_to_none_assignment(self):
        """Test assigning None to None variable (should be allowed)."""
        source = '''
        def main() {
            None x = None
            None y = None
            x = y
            print("x =", x)
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        # Capture output
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        output = f.getvalue().strip()
        assert "x = None" in output

    def test_none_type_enforcement_string_assignment(self):
        """Test that assigning string to None variable raises error."""
        source = '''
        def main() {
            None x = None
            x = "Aeonath"
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'x': expected None, got str" in error_msg

    def test_none_type_enforcement_int_assignment(self):
        """Test that assigning int to None variable raises error."""
        source = '''
        def main() {
            None x = None
            x = 42
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'x': expected None, got int" in error_msg

    def test_none_type_enforcement_float_assignment(self):
        """Test that assigning float to None variable raises error."""
        source = '''
        def main() {
            None x = None
            x = 3.14
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'x': expected None, got float" in error_msg

    def test_none_type_enforcement_bool_assignment(self):
        """Test that assigning bool to None variable raises error."""
        source = '''
        def main() {
            None x = None
            x = true
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'x': expected None, got bool" in error_msg

    def test_none_type_enforcement_list_assignment(self):
        """Test that assigning list to None variable raises error."""
        source = '''
        def main() {
            None x = None
            x = [1, 2, 3]
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'x': expected None, got list" in error_msg

    def test_none_type_enforcement_dict_assignment(self):
        """Test that assigning dict to None variable raises error."""
        source = '''
        def main() {
            None x = None
            x = {"key": "value"}
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'x': expected None, got dict" in error_msg

    def test_none_function_parameter_enforcement(self):
        """Test None type enforcement in function parameters."""
        source = '''
        def None process_none(None value) {
            return value
        }
        
        def main() {
            None x = None
            result = process_none(x)
            print("result =", result)
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        # Capture output
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        output = f.getvalue().strip()
        assert "result = None" in output

    def test_none_function_parameter_type_error(self):
        """Test that passing non-None to None parameter raises error."""
        source = '''
        def None process_none(None value) {
            return value
        }
        
        def main() {
            result = process_none("hello")
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for parameter 'value': expected None, got str" in error_msg

    def test_none_function_return_type_enforcement(self):
        """Test None return type enforcement."""
        source = '''
        def None get_none() {
            return None
        }
        
        def main() {
            None result = get_none()
            print("result =", result)
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        # Capture output
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        output = f.getvalue().strip()
        assert "result = None" in output

    def test_none_function_return_type_error(self):
        """Test that returning non-None from None function raises error."""
        source = '''
        def None get_none() {
            return "hello"
        }
        
        def main() {
            result = get_none()
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "return type mismatch: expected None, got str" in error_msg

    def test_mixed_none_and_typed_variables(self):
        """Test mixing None and typed variables in the same scope."""
        source = '''
        def main() {
            None x = None
            int y = 42
            str z = "hello"
            
            print("x =", x)
            print("y =", y)
            print("z =", z)
            
            # This should work
            x = None
            
            # This should fail
            y = None
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'y': expected int, got None" in error_msg

    def test_none_comprehensive_scenarios(self):
        """Test comprehensive None type scenarios."""
        source = '''
        def None process_data(None data) {
            if data == None:
                return None
            else:
                return data
            end
        }
        
        def main() {
            None x = None
            None y = None
            
            # Valid assignments
            x = y
            y = process_data(x)
            
            print("x =", x)
            print("y =", y)
            
            # This should fail - trying to assign string to None variable
            x = "invalid"
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'x': expected None, got str" in error_msg
