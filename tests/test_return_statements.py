"""
Tests for Sprint 3 Task 2 - Return Statements and Function Values
"""

import pytest
from lyric.parser import parse
from lyric.interpreter import interpret
from lyric.errors import RuntimeErrorLyric


class TestReturnStatements:
    """Test return statement and function value functionality."""

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

    def test_return_values_assigned_to_variables(self):
        """Test A5: Functions can return values and assign them to variables."""
        source = '''
def get_five() {
    return 5
}

def add(a, b) {
    return a + b
}

def get_string() {
    return "hello"
}

def main() {
    x = get_five()
    y = add(10, 20)
    z = get_string()
    
    print("x =", x)
    print("y =", y)
    print("z =", z)
}
'''
        output = self.capture_output(source)
        assert "x = 5" in output
        assert "y = 30" in output
        assert "z = hello" in output

    def test_print_function_calls(self):
        """Test A6: print(add(2,3)) outputs the correct numeric result."""
        source = '''
def add(a, b) {
    return a + b
}

def get_five() {
    return 5
}

def main() {
    print("add(2,3) =", add(2, 3))
    print("add(5,7) =", add(5, 7))
    print("get_five() =", get_five())
}
'''
        output = self.capture_output(source)
        assert "add(2,3) = 5" in output
        assert "add(5,7) = 12" in output
        assert "get_five() = 5" in output

    def test_missing_return_defaults_to_none(self):
        """Test A7: Missing return defaults to None."""
        source = '''
def get_nothing() {
    # No return statement
}

def main() {
    result = get_nothing()
    print("result =", result)
    print("is None?", result == None)
}
'''
        output = self.capture_output(source)
        assert "result = None" in output
        assert "is None? True" in output

    def test_return_none_explicitly(self):
        """Test explicit return None."""
        source = '''
def explicit_none() {
    return None
}

def main() {
    result = explicit_none()
    print("result =", result)
    print("is None?", result == None)
}
'''
        output = self.capture_output(source)
        assert "result = None" in output
        assert "is None? True" in output

    def test_function_values_in_expressions(self):
        """Test function return values used in complex expressions."""
        source = '''
def get_five() {
    return 5
}

def add(a, b) {
    return a + b
}

def get_string() {
    return "hello"
}

def main() {
    # Function calls in arithmetic expressions
    result1 = add(get_five(), get_five())
    result2 = add(1, add(2, 3))
    
    # Function calls in string expressions
    result3 = get_string() + " world"
    
    print("add(get_five(), get_five()) =", result1)
    print("add(1, add(2, 3)) =", result2)
    print("get_string() + ' world' =", result3)
}
'''
        output = self.capture_output(source)
        assert "add(get_five(), get_five()) = 10" in output
        assert "add(1, add(2, 3)) = 6" in output
        assert "get_string() + ' world' = hello world" in output

    def test_nested_function_calls(self):
        """Test nested function calls with return values."""
        source = '''
def outer(x) {
    return x * 2
}

def inner(y) {
    return y + 1
}

def main() {
    result = outer(inner(5))
    print("outer(inner(5)) =", result)
    
    # Multiple levels of nesting
    result2 = outer(outer(inner(2)))
    print("outer(outer(inner(2))) =", result2)
}
'''
        output = self.capture_output(source)
        assert "outer(inner(5)) = 12" in output  # (5+1)*2 = 12
        assert "outer(outer(inner(2))) = 12" in output  # ((2+1)*2)*2 = 12

    def test_return_different_types(self):
        """Test returning different data types."""
        source = '''
def get_int() {
    return 42
}

def get_float() {
    return 3.14
}

def get_string() {
    return "hello"
}

def get_bool() {
    return true
}

def main() {
    print("int:", get_int(), "type:", type(get_int()))
    print("float:", get_float(), "type:", type(get_float()))
    print("string:", get_string(), "type:", type(get_string()))
    print("bool:", get_bool(), "type:", type(get_bool()))
}
'''
        output = self.capture_output(source)
        assert "int: 42 type: int" in output
        assert "float: 3.14 type: float" in output
        assert "string: hello type: str" in output
        assert "bool: True type: bool" in output

    def test_return_with_type_annotations(self):
        """Test return statements with type annotations (from Task 1)."""
        source = '''
def int get_int() {
    return 42
}

def int add(int a, int b) {
    return a + b
}

def str get_string() {
    return "hello"
}

def main() {
    x = get_int()
    y = add(5, 3)
    z = get_string()
    
    print("x =", x, "type:", type(x))
    print("y =", y, "type:", type(y))
    print("z =", z, "type:", type(z))
}
'''
        output = self.capture_output(source)
        assert "x = 42 type: int" in output
        assert "y = 8 type: int" in output
        assert "z = hello type: str" in output

    def test_return_type_enforcement(self):
        """Test return type enforcement with type annotations."""
        source = '''
def str get_string() {
    return 42
}

def main() {
    result = get_string()
}
'''
        program = parse(source, "test")
        
        with pytest.raises(RuntimeErrorLyric, match="Function 'get_string' return type mismatch"):
            interpret(program)

    def test_comprehensive_return_statements(self):
        """Test comprehensive return statement functionality."""
        source = '''
# Various return scenarios
def simple_return() {
    return 100
}

def expression_return() {
    return 10 + 20
}

    def conditional_return(x) {
        if x > 0:
            return 1
        else:
            return 0
        end
    }
    
    def no_return() {
        # No return statement
    }
    
    def main() {
        print("=== Return Statement Tests ===")
        
        # Simple return
        print("simple_return() =", simple_return())
        
        # Expression return
        print("expression_return() =", expression_return())
        
        # Conditional return
        print("conditional_return(5) =", conditional_return(5))
        print("conditional_return(-3) =", conditional_return(-3))
        
        # No return
        print("no_return() =", no_return())
        
        # Function calls in expressions
        x = simple_return() * 2
        y = expression_return() + conditional_return(0)
        
        print("simple_return() * 2 =", x)
        print("expression_return() + conditional_return(0) =", y)
        
        print("=== All Return Tests Passed ===")
    }
'''
        output = self.capture_output(source)
        assert "=== Return Statement Tests ===" in output
        assert "simple_return() = 100" in output
        assert "expression_return() = 30" in output
        assert "conditional_return(5) = 1" in output
        assert "conditional_return(-3) = 0" in output
        assert "no_return() = None" in output
        assert "simple_return() * 2 = 200" in output
        assert "=== All Return Tests Passed ===" in output
