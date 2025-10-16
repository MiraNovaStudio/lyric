"""
Tests for Sprint 3 Task 1 - Type Declaration and Inference
"""

import pytest
from lyric.lexer import tokenize
from lyric.parser import parse
from lyric.interpreter import interpret
from lyric.errors import RuntimeErrorLyric


class TestTypeSystem:
    """Test type declaration and inference functionality."""

    def capture_output(self, program_code):
        """Capture stdout from running a program."""
        import io
        import sys
        from contextlib import redirect_stdout

        # Parse the program code
        program = parse(program_code, "test")

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            interpret(program)
        finally:
            sys.stdout = old_stdout

        return captured_output.getvalue()

    def test_type_annotated_variable_assignment(self):
        """Test A1: Type declarations work correctly."""
        source = '''
x: int = 5
y: str = "hello"
z: bool = true

def main() {
    print("x:", x, "type:", type(x))
    print("y:", y, "type:", type(y))
    print("z:", z, "type:", type(z))
}
'''
        output = self.capture_output(source)
        assert "x: 5 type: int" in output
        assert "y: hello type: str" in output
        assert "z: True type: bool" in output

    def test_type_enforcement_variable(self):
        """Test A2: Assigning a string to a variable declared as int raises a runtime error."""
        source = '''
x: int = "hello"
'''
        program = parse(source, "test")
        
        with pytest.raises(RuntimeErrorLyric, match="Type mismatch: expected int, got str"):
            interpret(program)

    def test_type_annotated_function_parameters(self):
        """Test A3: Functions with typed parameters enforce types."""
        source = '''
def add(a: int, b: int): int {
    return a + b
}

def main() {
    result = add(5, 3)
    print("add(5, 3):", result)
}
'''
        output = self.capture_output(source)
        assert "add(5, 3): 8" in output

    def test_type_enforcement_function_parameters(self):
        """Test A3: Functions with typed parameters enforce types when called with wrong types."""
        source = '''
def add(a: int, b: int): int {
    return a + b
}

def main() {
    result = add("hello", "world")
}
'''
        program = parse(source, "test")
        
        with pytest.raises(RuntimeErrorLyric, match="Type mismatch: expected int, got str"):
            interpret(program)

    def test_type_inference_literals(self):
        """Test A4: Type inference assigns correct default types for literals."""
        source = '''
auto_int = 42
auto_float = 3.14
auto_string = "inferred"
auto_bool = false
auto_none = None

def main() {
    print("auto_int:", auto_int, "type:", type(auto_int))
    print("auto_float:", auto_float, "type:", type(auto_float))
    print("auto_string:", auto_string, "type:", type(auto_string))
    print("auto_bool:", auto_bool, "type:", type(auto_bool))
    print("auto_none:", auto_none, "type:", type(auto_none))
}
'''
        output = self.capture_output(source)
        assert "auto_int: 42 type: int" in output
        assert "auto_float: 3.14 type: float" in output
        assert "auto_string: inferred type: str" in output
        assert "auto_bool: False type: bool" in output
        assert "auto_none: None type: None" in output

    def test_return_type_enforcement(self):
        """Test return type enforcement."""
        source = '''
def get_string(): str {
    return 42
}

def main() {
    result = get_string()
}
'''
        program = parse(source, "test")
        
        with pytest.raises(RuntimeErrorLyric, match="Return type mismatch: expected str, got int"):
            interpret(program)

    def test_type_annotated_function_return(self):
        """Test type-annotated function with correct return type."""
        source = '''
def get_string(): str {
    return "hello"
}

def main() {
    result = get_string()
    print("result:", result, "type:", type(result))
}
'''
        output = self.capture_output(source)
        assert "result: hello type: str" in output

    def test_mixed_type_annotations(self):
        """Test mixing type-annotated and non-annotated variables."""
        source = '''
typed_var: int = 5
inferred_var = 10

def typed_func(x: int): int {
    return x * 2
}

def inferred_func(y) {
    return y + 1
}

def main() {
    print("typed_var:", typed_var, "type:", type(typed_var))
    print("inferred_var:", inferred_var, "type:", type(inferred_var))
    print("typed_func(3):", typed_func(3))
    print("inferred_func(7):", inferred_func(7))
}
'''
        output = self.capture_output(source)
        assert "typed_var: 5 type: int" in output
        assert "inferred_var: 10 type: int" in output
        assert "typed_func(3): 6" in output
        assert "inferred_func(7): 8" in output

    def test_comprehensive_type_system(self):
        """Test comprehensive type system functionality."""
        source = '''
# Type-annotated variables
counter: int = 0
message: str = "Type system working"
enabled: bool = true

    # Type-inferred variables
    auto_number = 100

# Type-annotated functions
def increment(x: int): int {
    return x + 1
}

def format_message(name: str): str {
    return message + ": " + name
}

def check_status(): bool {
    return enabled
}

def main() {
    print("=== Type System Test ===")
    
    # Test typed variables
    print("counter:", counter, "type:", type(counter))
    print("message:", message, "type:", type(message))
    print("enabled:", enabled, "type:", type(enabled))
    
    # Test inferred variables
    print("auto_number:", auto_number, "type:", type(auto_number))
    
    # Test typed functions
    print("increment(5):", increment(5))
    print("format_message('Alice'):", format_message("Alice"))
    print("check_status():", check_status())
    
    # Test type checking
    print("isinstance(counter, 'int'):", isinstance(counter, "int"))
    print("isinstance(message, 'str'):", isinstance(message, "str"))
    print("isinstance(enabled, 'bool'):", isinstance(enabled, "bool"))
    
    print("=== All Type Tests Passed ===")
}
'''
        output = self.capture_output(source)
        assert "=== Type System Test ===" in output
        assert "counter: 0 type: int" in output
        assert "message: Type system working type: str" in output
        assert "enabled: True type: bool" in output
        assert "auto_number: 100 type: int" in output
        assert "increment(5): 6" in output
        assert "format_message('Alice'): Type system working: Alice" in output
        assert "isinstance(counter, 'int'): True" in output
        assert "=== All Type Tests Passed ===" in output
