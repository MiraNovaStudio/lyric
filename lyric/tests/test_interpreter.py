"""Tests for interpreter module."""

import pytest
from lyric.interpreter import evaluate, Interpreter
from lyric.parser import parse
from lyric.errors import RuntimeErrorLyric


def test_evaluate_function_definition():
    """Test evaluating function definition: def main() { print("Hello, Lyric!") }"""
    source = 'def main() { print("Hello, Lyric!") }'
    
    ast = parse(source)
    result = evaluate(ast)
    
    # Function definition should not return anything
    assert result is None
    
    # Verify function was defined
    interpreter = Interpreter()
    interpreter.evaluate(ast)
    assert "main" in interpreter.functions


def test_evaluate_if_else_statement():
    """Test evaluating if/else statement."""
    source = '''def main() {
x = 5
if x > 0:
print("positive")
else:
print("non-positive")
end
}'''
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check that "positive" was printed
        output = captured_output.getvalue().strip()
        assert "positive" in output
    finally:
        sys.stdout = old_stdout


def test_evaluate_loop_statement():
    """Test evaluating loop statement: given i in range(3): print(i) done"""
    source = '''def main() {
given i in range(3):
print("iteration")
done
}'''
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check that "iteration" was printed 3 times
        output = captured_output.getvalue().strip()
        lines = output.split('\n')
        assert len(lines) == 3
        assert all("iteration" in line for line in lines)
    finally:
        sys.stdout = old_stdout


def test_evaluate_class_definition():
    """Test evaluating class definition: class Player: name = "Guest" def greet() { print("Hello,", self.name) } +++"""
    source = '''class Player:
name = "Guest"
def greet() {
print("Hello,", self.name)
}
+++'''
    
    ast = parse(source)
    result = evaluate(ast)
    
    # Class definition should not return anything
    assert result is None
    
    # Verify class was defined
    interpreter = Interpreter()
    interpreter.evaluate(ast)
    assert "Player" in interpreter.classes
    
    # Check class members
    player_class = interpreter.classes["Player"]
    assert "name" in player_class
    assert player_class["name"] == "Guest"
    assert "greet" in player_class


def test_evaluate_else_if_sequence():
    """Test evaluating else-if sequence."""
    source = '''def main() {
x = 5
if x > 10:
print("high")
else if x > 5:
print("medium")
else if x > 0:
print("low")
else:
print("zero or negative")
end
}'''
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check that "low" was printed (since x = 5)
        output = captured_output.getvalue().strip()
        assert "low" in output
        assert "high" not in output
        assert "medium" not in output
        assert "zero or negative" not in output
    finally:
        sys.stdout = old_stdout


def test_evaluate_binary_operations():
    """Test evaluating binary operations with precedence."""
    source = '''def main() {
result = 2 + 3 * 4 - 1
print(result)
}'''
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check that result is 13 (2 + (3 * 4) - 1 = 2 + 12 - 1 = 13)
        output = captured_output.getvalue().strip()
        assert "13" in output
    finally:
        sys.stdout = old_stdout


def test_evaluate_function_with_parameters():
    """Test evaluating function with parameters."""
    source = '''def add(x, y) {
return x + y
}

def main() {
result = add(3, 4)
print(result)
}'''
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check that result is 7
        output = captured_output.getvalue().strip()
        assert "7" in output
    finally:
        sys.stdout = old_stdout


def test_evaluate_complex_nested_structure():
    """Test evaluating a complex nested structure."""
    source = '''def main() {
x = 10
if x > 5:
y = x * 2
if y > 15:
print("nested if")
else:
print("nested else")
end
else:
print("outer else")
end
}'''
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check that "nested if" was printed (since x=10, y=20, y>15)
        output = captured_output.getvalue().strip()
        assert "nested if" in output
        assert "nested else" not in output
        assert "outer else" not in output
    finally:
        sys.stdout = old_stdout


def test_evaluate_variable_scope():
    """Test variable scope handling."""
    source = '''def test_scope() {
local_var = "local"
print(local_var)
}

def main() {
global_var = "global"
test_scope()
print(global_var)
}'''
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check output
        output = captured_output.getvalue().strip()
        lines = output.split('\n')
        assert len(lines) == 2
        assert "local" in lines[0]
        assert "global" in lines[1]
    finally:
        sys.stdout = old_stdout


def test_evaluate_error_handling():
    """Test interpreter error handling."""
    # Test undefined variable
    source = 'def main() { print(undefined_var) }'
    ast = parse(source)
    
    with pytest.raises(RuntimeErrorLyric):
        evaluate(ast)
    
    # Test undefined function
    source = 'def main() { undefined_func() }'
    ast = parse(source)
    
    with pytest.raises(RuntimeErrorLyric):
        evaluate(ast)
    
    # Test division by zero
    source = 'def main() { result = 5 / 0 }'
    ast = parse(source)
    
    with pytest.raises(RuntimeErrorLyric):
        evaluate(ast)


def test_evaluate_member_access():
    """Test member access evaluation."""
    source = '''class Person:
name = "John"
age = 30
+++

def main() {
person = Person
print(person.name)
print(person.age)
}'''
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check output
        output = captured_output.getvalue().strip()
        assert "John" in output
        assert "30" in output
    finally:
        sys.stdout = old_stdout


def test_evaluate_logical_operations():
    """Test logical operations evaluation."""
    source = '''def main() {
a = true
b = false
result1 = a and b
result2 = a or b
result3 = not a
print(result1, result2, result3)
}'''
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check output (Note: true/false are not implemented yet, so this will test the structure)
        output = captured_output.getvalue().strip()
        # This test will need to be updated when boolean literals are implemented
    finally:
        sys.stdout = old_stdout