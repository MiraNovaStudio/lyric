"""
Test suite for god type functionality - SPRINT5 Task 7
Tests the new god type (boolean type honoring Kurt Gödel)
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
from lyric.errors import LexError, ParseError, RuntimeErrorLyric


class TestGodType:
    """Test god type functionality."""

    def capture_output(self, source: str) -> str:
        """Capture output from running Lyric source code."""
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        return f.getvalue()

    def test_god_basic_declaration(self):
        """Test basic god type declaration with true/false literals."""
        source = '''
def main() {
    god ready = true
    god not_ready = false
    print("Ready:", ready)
    print("Not ready:", not_ready)
    print("Ready type:", type(ready))
    print("Not ready type:", type(not_ready))
}
'''
        output = self.capture_output(source)
        assert "Ready: True" in output
        assert "Not ready: False" in output
        assert "Ready type: god" in output
        assert "Not ready type: god" in output

    def test_god_conditional_statements(self):
        """Test god type in conditional statements."""
        source = '''
def main() {
    god condition = true
    if condition:
        print("Condition is true")
    else:
        print("Condition is false")
    end
    
    god false_condition = false
    if false_condition:
        print("This should not print")
    else:
        print("Condition is false")
    end
}
'''
        output = self.capture_output(source)
        assert "Condition is true" in output
        assert "Condition is false" in output
        assert "This should not print" not in output

    def test_god_logical_operations(self):
        """Test god type with logical operations (and, or, not)."""
        source = '''
def main() {
    god a = true
    god b = false
    
    var result_and = a and b
    var result_or = a or b
    var result_not_a = not a
    var result_not_b = not b
    
    print("a and b:", result_and)
    print("a or b:", result_or)
    print("not a:", result_not_a)
    print("not b:", result_not_b)
    
    print("result_and type:", type(result_and))
    print("result_or type:", type(result_or))
}
'''
        output = self.capture_output(source)
        assert "a and b: False" in output
        assert "a or b: True" in output
        assert "not a: False" in output
        assert "not b: True" in output
        assert "result_and type: god" in output
        assert "result_or type: god" in output

    def test_god_comparison_operations(self):
        """Test god type with comparison operations."""
        source = '''
def main() {
    var x = 5
    var y = 10
    
    god equal_result = x == y
    god not_equal_result = x != y
    god less_result = x < y
    god greater_result = x > y
    
    print("x == y:", equal_result)
    print("x != y:", not_equal_result)
    print("x < y:", less_result)
    print("x > y:", greater_result)
    
    print("equal_result type:", type(equal_result))
}
'''
        output = self.capture_output(source)
        assert "x == y: False" in output
        assert "x != y: True" in output
        assert "x < y: True" in output
        assert "x > y: False" in output
        assert "equal_result type: god" in output

    def test_god_simple_function_return(self):
        """Test god type with simple function (without typed parameters)."""
        source = '''
def is_even(number) {
    return number % 2 == 0
}

def main() {
    god result1 = is_even(4)
    god result2 = is_even(5)
    
    print("is_even(4):", result1)
    print("is_even(5):", result2)
    
    print("result1 type:", type(result1))
}
'''
        output = self.capture_output(source)
        assert "is_even(4): True" in output
        assert "is_even(5): False" in output
        assert "result1 type: god" in output

    def test_god_multi_declaration(self):
        """Test god type in multi-variable declarations."""
        source = '''
def main() {
    god flag1, god flag2, god flag3
    flag1 = true
    flag2 = false
    flag3 = true
    
    print("flag1:", flag1)
    print("flag2:", flag2)
    print("flag3:", flag3)
    
    print("flag1 type:", type(flag1))
    print("flag2 type:", type(flag2))
    print("flag3 type:", type(flag3))
}
'''
        output = self.capture_output(source)
        assert "flag1: True" in output
        assert "flag2: False" in output
        assert "flag3: True" in output
        assert "flag1 type: god" in output
        assert "flag2 type: god" in output
        assert "flag3 type: god" in output

    def test_god_mixed_multi_declaration(self):
        """Test god type in mixed multi-variable declarations."""
        source = '''
def main() {
    var x, int y, god flag, str name
    x = 3.14
    y = 42
    flag = true
    name = "test"
    
    print("x:", x, "type:", type(x))
    print("y:", y, "type:", type(y))
    print("flag:", flag, "type:", type(flag))
    print("name:", name, "type:", type(name))
}
'''
        output = self.capture_output(source)
        assert "x: 3.14 type: float" in output
        assert "y: 42 type: int" in output
        assert "flag: True type: god" in output
        assert "name: test type: str" in output

    def test_god_type_inference(self):
        """Test god type inference for boolean literals."""
        source = '''
def main() {
    var auto_true = true
    var auto_false = false
    
    print("auto_true:", auto_true, "type:", type(auto_true))
    print("auto_false:", auto_false, "type:", type(auto_false))
}
'''
        output = self.capture_output(source)
        assert "auto_true: True type: god" in output
        assert "auto_false: False type: god" in output

    def test_god_while_loop_condition(self):
        """Test god type in while loop conditions."""
        source = '''
def main() {
    var count = 0
    god keep_going = true
    
    given keep_going:
        print("Count:", count)
        count = count + 1
        if count >= 3:
            keep_going = false
        end
    done
    
    print("Final count:", count)
}
'''
        output = self.capture_output(source)
        assert "Count: 0" in output
        assert "Count: 1" in output
        assert "Count: 2" in output
        assert "Final count: 3" in output

    def test_god_complex_logical_expressions(self):
        """Test complex logical expressions with god type."""
        source = '''
def main() {
    var age = 25
    var has_license = true
    var has_insurance = false
    
    god can_drive = age >= 18 and has_license
    god needs_insurance = can_drive and not has_insurance
    god complex_condition = (age > 20 or has_license) and has_insurance
    
    print("can_drive:", can_drive)
    print("needs_insurance:", needs_insurance)
    print("complex_condition:", complex_condition)
    
    print("can_drive type:", type(can_drive))
}
'''
        output = self.capture_output(source)
        assert "can_drive: True" in output
        assert "needs_insurance: True" in output
        assert "complex_condition: False" in output
        assert "can_drive type: god" in output

    def test_god_type_enforcement(self):
        """Test type enforcement for god type."""
        source = '''
def main() {
    god flag = true
    flag = false  # Should work
    print("flag after assignment:", flag)
    
    # This should cause a type error
    flag = 42
    print("This should not print")
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            self.capture_output(source)
        assert "Type mismatch" in str(exc_info.value)

    def test_god_truthiness_evaluation(self):
        """Test truthiness evaluation of god type."""
        source = '''
def main() {
    god true_value = true
    god false_value = false
    
    if true_value:
        print("true_value is truthy")
    end
    
    if false_value:
        print("This should not print")
    else:
        print("false_value is falsy")
    end
}
'''
        output = self.capture_output(source)
        assert "true_value is truthy" in output
        assert "false_value is falsy" in output
        assert "This should not print" not in output
