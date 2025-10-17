"""
Test suite for type enforcement verification - SPRINT6 Task 2
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


class TestTypeEnforcementVerification:
    """Test comprehensive type enforcement for all declared types."""

    def capture_output(self, source: str) -> str:
        """Capture output from running Lyric source code."""
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        return f.getvalue()

    def test_int_type_enforcement_success(self):
        """Test successful int type assignments."""
        source = '''
def main() {
    int x = 42
    print("x:", x, "type:", type(x))
    
    x = 100
    print("x after reassignment:", x)
}
'''
        output = self.capture_output(source)
        assert "x: 42" in output
        assert "type: int" in output
        assert "x after reassignment: 100" in output

    def test_int_type_enforcement_failure(self):
        """Test int type enforcement with clear error messages."""
        source = '''
def main() {
    int x = 42
    x = "hello"
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'x'" in error_msg
        assert "expected int" in error_msg
        assert "got str" in error_msg

    def test_str_type_enforcement_success(self):
        """Test successful str type assignments."""
        source = '''
def main() {
    str name = "Alice"
    print("name:", name, "type:", type(name))
    
    name = "Bob"
    print("name after reassignment:", name)
}
'''
        output = self.capture_output(source)
        assert "name: Alice" in output
        assert "type: str" in output
        assert "name after reassignment: Bob" in output

    def test_str_type_enforcement_failure(self):
        """Test str type enforcement with clear error messages."""
        source = '''
def main() {
    str name = "Alice"
    name = 42
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'name'" in error_msg
        assert "expected str" in error_msg
        assert "got int" in error_msg

    def test_float_type_enforcement_success(self):
        """Test successful float type assignments."""
        source = '''
def main() {
    float pi = 3.14
    print("pi:", pi, "type:", type(pi))
    
    pi = 2.71
    print("pi after reassignment:", pi)
}
'''
        output = self.capture_output(source)
        assert "pi: 3.14" in output
        assert "type: float" in output
        assert "pi after reassignment: 2.71" in output

    def test_float_type_enforcement_failure(self):
        """Test float type enforcement with clear error messages."""
        source = '''
def main() {
    float pi = 3.14
    pi = "not a number"
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'pi'" in error_msg
        assert "expected float" in error_msg
        assert "got str" in error_msg

    def test_god_type_enforcement_success(self):
        """Test successful god (boolean) type assignments."""
        source = '''
def main() {
    god flag = true
    print("flag:", flag, "type:", type(flag))
    
    flag = false
    print("flag after reassignment:", flag)
}
'''
        output = self.capture_output(source)
        assert "flag: True" in output
        assert "type: god" in output
        assert "flag after reassignment: False" in output

    def test_god_type_enforcement_failure(self):
        """Test god type enforcement with clear error messages."""
        source = '''
def main() {
    god flag = true
    flag = 42
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'flag'" in error_msg
        assert "expected god" in error_msg
        assert "got int" in error_msg

    def test_rex_type_enforcement_success(self):
        """Test successful rex type assignments."""
        source = '''
def main() {
    rex pattern = /^hello/
    print("pattern:", pattern, "type:", type(pattern))
    
    pattern = /world$/
    print("pattern after reassignment:", pattern)
}
'''
        output = self.capture_output(source)
        assert "pattern: ^hello" in output
        assert "type: rex" in output
        assert "pattern after reassignment: world$" in output

    def test_rex_type_enforcement_failure(self):
        """Test rex type enforcement with clear error messages."""
        source = '''
def main() {
    rex pattern = /^hello/
    pattern = "not a regex"
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'pattern'" in error_msg
        assert "expected rex" in error_msg
        assert "got str" in error_msg

    def test_var_type_flexibility(self):
        """Test var type allows any value type."""
        source = '''
def main() {
    var x = 42
    print("x as int:", x, "type:", type(x))
    
    x = "hello"
    print("x as str:", x, "type:", type(x))
    
    x = true
    print("x as god:", x, "type:", type(x))
    
    x = 3.14
    print("x as float:", x, "type:", type(x))
}
'''
        output = self.capture_output(source)
        assert "x as int: 42" in output
        assert "x as str: hello" in output
        assert "x as god: True" in output
        assert "x as float: 3.14" in output

    def test_function_return_type_enforcement_success(self):
        """Test successful function return type enforcement."""
        source = '''
def int get_number() {
    return 42
}

def str get_message() {
    return "hello"
}

def main() {
    var num = get_number()
    var msg = get_message()
    print("Number:", num, "type:", type(num))
    print("Message:", msg, "type:", type(msg))
}
'''
        output = self.capture_output(source)
        assert "Number: 42" in output
        assert "Message: hello" in output

    def test_function_return_type_enforcement_failure(self):
        """Test function return type enforcement with clear error messages."""
        source = '''
def int get_number() {
    return "not a number"
}

def main() {
    var num = get_number()
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Function 'get_number' return type mismatch" in error_msg
        assert "expected int" in error_msg
        assert "got str" in error_msg

    def test_function_parameter_type_enforcement_success(self):
        """Test successful function parameter type enforcement."""
        source = '''
def str greet(int age) {
    return "Age: " + str(age)
}

def main() {
    var message = greet(25)
    print("Message:", message)
}
'''
        output = self.capture_output(source)
        assert "Message: Age: 25" in output

    def test_function_parameter_type_enforcement_failure(self):
        """Test function parameter type enforcement with clear error messages."""
        source = '''
def str greet(int age) {
    return "Age: " + str(age)
}

def main() {
    var message = greet("not a number")
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "In function 'greet':" in error_msg
        assert "Type mismatch for parameter 'age'" in error_msg
        assert "expected int" in error_msg
        assert "got str" in error_msg

    def test_mixed_type_assignments(self):
        """Test mixed type assignments in the same scope."""
        source = '''
def main() {
    int x = 10
    str y = "hello"
    god z = true
    float w = 3.14
    
    print("x:", x, "type:", type(x))
    print("y:", y, "type:", type(y))
    print("z:", z, "type:", type(z))
    print("w:", w, "type:", type(w))
    
    # Reassignments with same types
    x = 20
    y = "world"
    z = false
    w = 2.71
    
    print("After reassignment:")
    print("x:", x, "type:", type(x))
    print("y:", y, "type:", type(y))
    print("z:", z, "type:", type(z))
    print("w:", w, "type:", type(w))
}
'''
        output = self.capture_output(source)
        assert "x: 10" in output
        assert "y: hello" in output
        assert "z: True" in output
        assert "w: 3.14" in output
        assert "x: 20" in output
        assert "y: world" in output
        assert "z: False" in output
        assert "w: 2.71" in output

    def test_no_silent_type_coercions(self):
        """Test that no silent type coercions occur."""
        source = '''
def main() {
    int x = 42
    
    # These should all fail with clear error messages
    x = "42"      # String to int
    x = 3.14      # Float to int
    x = true      # Boolean to int
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'x'" in error_msg
        assert "expected int" in error_msg
        assert "got str" in error_msg  # First assignment should fail

    def test_nested_scope_type_enforcement(self):
        """Test type enforcement in nested scopes."""
        source = '''
def main() {
    int x = 10
    print("Outer x:", x, "type:", type(x))
    
    if true:
        str x = "inner"
        print("Inner x:", x, "type:", type(x))
        
        # This should fail - trying to assign int to str
        x = 42
    end
    
    print("Outer x after block:", x, "type:", type(x))
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'x'" in error_msg
        assert "expected str" in error_msg
        assert "got int" in error_msg

    def test_list_and_dict_type_enforcement(self):
        """Test list and dict type enforcement."""
        source = '''
def main() {
    list numbers = [1, 2, 3]
    dict person = {"name": "Alice", "age": 30}
    
    print("numbers:", numbers, "type:", type(numbers))
    print("person:", person, "type:", type(person))
    
    # These should fail
    numbers = "not a list"
    person = 42
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'numbers'" in error_msg
        assert "expected list" in error_msg
        assert "got str" in error_msg

    def test_none_type_enforcement(self):
        """Test None type enforcement."""
        source = '''
def main() {
    None value = None
    print("value:", value, "type:", type(value))
    
    # This should fail
    value = "not none"
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'value'" in error_msg
        assert "expected None" in error_msg
        assert "got str" in error_msg


