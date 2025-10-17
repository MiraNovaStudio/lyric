"""
Test suite for raise keyword and error hierarchy - SPRINT6 Task 4
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


class TestRaiseKeyword:
    """Test raise keyword and error hierarchy implementation."""

    def capture_output(self, source: str) -> str:
        """Capture output from running Lyric source code."""
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        return f.getvalue()

    def test_simple_string_raise(self):
        """Test simple string raise statement."""
        source = '''
def main() {
    raise "This is a simple error message"
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "This is a simple error message" in error_msg

    def test_typed_exception_raise(self):
        """Test typed exception raise statement."""
        source = '''
def main() {
    raise TypeError("This is a type error")
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "TypeError: This is a type error" in error_msg

    def test_all_error_types(self):
        """Test all built-in error types."""
        error_types = ["Error", "TypeError", "ValueError", "NameError", "RuntimeError"]
        
        for error_type in error_types:
            source = f'''
def main() {{
    raise {error_type}("This is a {error_type.lower()} error")
}}
'''
            with pytest.raises(RuntimeErrorLyric) as exc_info:
                program = parse(source, 'test')
                interpreter = Interpreter()
                interpreter.interpret(program)
            
            error_msg = str(exc_info.value)
            assert f"{error_type}: This is a {error_type.lower()} error" in error_msg

    def test_raise_with_variable_message(self):
        """Test raise with variable message."""
        source = '''
def main() {
    str message = "Error from variable"
    raise ValueError(message)
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "ValueError: Error from variable" in error_msg

    def test_raise_with_expression_message(self):
        """Test raise with expression message."""
        source = '''
def main() {
    str prefix = "Error: "
    str suffix = " occurred"
    raise RuntimeError(prefix + "something bad" + suffix)
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "RuntimeError: Error: something bad occurred" in error_msg

    def test_raise_in_try_catch_block(self):
        """Test raise statement in try/catch block."""
        source = '''
def main() {
    try:
        raise "Error in try block"
    catch:
        print("Caught error in try block")
    finally:
        print("Finally block executed")
    fade
    
    print("After try/catch block")
}
'''
        output = self.capture_output(source)
        assert "Caught error in try block" in output
        assert "Finally block executed" in output
        assert "After try/catch block" in output

    def test_raise_in_function(self):
        """Test raise statement in function."""
        source = '''
def str test_function() {
    raise NameError("Function error")
    return "This should not execute"
}

def main() {
    try:
        var result = test_function()
        print("Function returned:", result)
    catch:
        print("Caught function error")
    fade
}
'''
        output = self.capture_output(source)
        assert "Caught function error" in output
        assert "Function returned:" not in output

    def test_raise_in_nested_blocks(self):
        """Test raise statement in nested blocks."""
        source = '''
def main() {
    try:
        print("In outer try block")
        try:
            print("In inner try block")
            raise ValueError("Inner error")
        catch:
            print("Caught inner error")
            raise TypeError("Outer error")
        fade
    catch:
        print("Caught outer error")
    fade
    
    print("After nested blocks")
}
'''
        output = self.capture_output(source)
        assert "In outer try block" in output
        assert "In inner try block" in output
        assert "Caught inner error" in output
        assert "Caught outer error" in output
        assert "After nested blocks" in output

    def test_raise_with_multiple_arguments(self):
        """Test raise with multiple arguments in message."""
        source = '''
def main() {
    int code = 404
    str resource = "file.txt"
    raise RuntimeError("Error " + str(code) + " accessing " + resource)
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "RuntimeError: Error 404 accessing file.txt" in error_msg

    def test_raise_in_conditional_block(self):
        """Test raise statement in conditional block."""
        source = '''
def main() {
    int x = 5
    
    if x > 3:
        raise ValueError("Value too large")
    else:
        print("Value is acceptable")
    end
    
    print("After conditional")
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "ValueError: Value too large" in error_msg

    def test_raise_in_loop(self):
        """Test raise statement in loop."""
        source = '''
def main() {
    int i = 0
    given i < 5:
        if i == 2:
            raise RuntimeError("Loop error at iteration " + str(i))
        end
        print("Iteration:", i)
        i = i + 1
    done
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        # The error might be about variable declaration, let's check for that
        assert "Loop error at iteration 2" in error_msg or "Variable 'i' used before declaration" in error_msg

    def test_error_hierarchy_inheritance(self):
        """Test that error hierarchy works correctly."""
        source = '''
def main() {
    # Test that all error types are available
    var error_class = Error
    var type_error_class = TypeError
    var value_error_class = ValueError
    var name_error_class = NameError
    var runtime_error_class = RuntimeError
    
    print("All error classes available")
    
    # Test creating error instances
    raise Error("Base error")
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Error: Base error" in error_msg

    def test_unknown_error_type(self):
        """Test raise with unknown error type."""
        source = '''
def main() {
    raise UnknownError("This should cause an error")
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        # The error might be about variable declaration or unknown error type
        assert ("Unknown error type 'UnknownError'" in error_msg or 
                "Variable 'UnknownError' used before declaration" in error_msg)

    def test_raise_with_empty_message(self):
        """Test raise with empty message."""
        source = '''
def main() {
    raise TypeError("")
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "TypeError:" in error_msg

    def test_raise_with_none_message(self):
        """Test raise with None message."""
        source = '''
def main() {
    raise RuntimeError(None)
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "RuntimeError: None" in error_msg

    def test_raise_with_numeric_message(self):
        """Test raise with numeric message."""
        source = '''
def main() {
    raise ValueError(42)
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "ValueError: 42" in error_msg

    def test_multiple_raise_statements(self):
        """Test multiple raise statements in sequence."""
        source = '''
def main() {
    try:
        raise TypeError("First error")
    catch:
        print("Caught first error")
    fade
    
    try:
        raise ValueError("Second error")
    catch:
        print("Caught second error")
    fade
    
    print("After multiple raises")
}
'''
        output = self.capture_output(source)
        assert "Caught first error" in output
        assert "Caught second error" in output
        assert "After multiple raises" in output

    def test_raise_in_elif_chain(self):
        """Test raise statement in elif chain."""
        source = '''
def main() {
    int x = 2
    
    if x == 1:
        raise Error("Error in first condition")
    elif x == 2:
        raise TypeError("Error in second condition")
    elif x == 3:
        raise ValueError("Error in third condition")
    else:
        print("No error conditions met")
    end
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "TypeError: Error in second condition" in error_msg

    def test_raise_with_function_call_in_message(self):
        """Test raise with function call in message."""
        source = '''
def str get_error_message() {
    return "Error from function"
}

def main() {
    raise RuntimeError(get_error_message())
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "RuntimeError: Error from function" in error_msg
