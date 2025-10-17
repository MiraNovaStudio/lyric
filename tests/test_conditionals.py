"""
Test suite for conditional statements including if/elif/else - SPRINT6 PIVOT 6.3.1
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


class TestConditionals:
    """Test conditional statements including if/elif/else chains."""

    def capture_output(self, source: str) -> str:
        """Capture output from running Lyric source code."""
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        return f.getvalue()

    def test_simple_if_elif_else_chain(self):
        """Test simple chained if/elif/else with correct fall-through prevention."""
        source = '''
def main() {
    int x = 2
    
    if x == 1:
        print("x is 1")
    elif x == 2:
        print("x is 2")
    elif x == 3:
        print("x is 3")
    else:
        print("x is something else")
    end
    
    print("After if chain")
}
'''
        output = self.capture_output(source)
        assert "x is 2" in output
        assert "After if chain" in output
        # Ensure only one branch executes
        assert output.count("x is") == 1
        assert "x is 1" not in output
        assert "x is 3" not in output
        assert "x is something else" not in output

    def test_elif_chain_first_condition_true(self):
        """Test elif chain where first condition is true."""
        source = '''
def main() {
    int x = 1
    
    if x == 1:
        print("x is 1")
    elif x == 2:
        print("x is 2")
    elif x == 3:
        print("x is 3")
    else:
        print("x is something else")
    end
}
'''
        output = self.capture_output(source)
        assert "x is 1" in output
        # Ensure only first branch executes
        assert output.count("x is") == 1

    def test_elif_chain_last_condition_true(self):
        """Test elif chain where last elif condition is true."""
        source = '''
def main() {
    int x = 3
    
    if x == 1:
        print("x is 1")
    elif x == 2:
        print("x is 2")
    elif x == 3:
        print("x is 3")
    else:
        print("x is something else")
    end
}
'''
        output = self.capture_output(source)
        assert "x is 3" in output
        # Ensure only last elif executes
        assert output.count("x is") == 1

    def test_elif_chain_else_executes(self):
        """Test elif chain where else clause executes."""
        source = '''
def main() {
    int x = 5
    
    if x == 1:
        print("x is 1")
    elif x == 2:
        print("x is 2")
    elif x == 3:
        print("x is 3")
    else:
        print("x is something else")
    end
}
'''
        output = self.capture_output(source)
        assert "x is something else" in output
        # Ensure only else executes
        assert output.count("x is") == 1

    def test_nested_conditionals(self):
        """Test nested if/elif/else blocks."""
        source = '''
def main() {
    int x = 2
    int y = 3
    
    if x == 2:
        print("x is 2")
        if y == 3:
            print("nested: y is 3")
        elif y == 4:
            print("nested: y is 4")
        else:
            print("nested: y is something else")
        end
    elif x == 3:
        print("x is 3")
    else:
        print("x is something else")
    end
    
    print("After nested conditionals")
}
'''
        output = self.capture_output(source)
        assert "x is 2" in output
        assert "nested: y is 3" in output
        assert "After nested conditionals" in output
        # Ensure correct fall-through
        assert output.count("nested:") == 1

    def test_mixed_conditions_with_and_or_operators(self):
        """Test complex conditions using and/or operators."""
        source = '''
def main() {
    int age = 25
    god is_student = true
    god has_job = false
    
    if age < 18:
        print("Minor")
    elif age >= 18 and age < 65:
        print("Adult")
    elif age >= 65:
        print("Senior")
    else:
        print("Invalid age")
    end
    
    if is_student and age >= 18:
        print("Adult student")
    elif is_student and age < 18:
        print("Minor student")
    elif not is_student and has_job:
        print("Working adult")
    elif not is_student and not has_job:
        print("Unemployed adult")
    else:
        print("Other status")
    end
}
'''
        output = self.capture_output(source)
        assert "Adult" in output
        assert "Adult student" in output
        # Ensure correct execution flow
        assert output.count("Adult") == 2
        assert "Minor" not in output
        assert "Senior" not in output
        assert "Working adult" not in output
        assert "Unemployed adult" not in output

    def test_string_conditions(self):
        """Test elif chains with string conditions."""
        source = '''
def main() {
    str grade = "B"
    
    if grade == "A":
        print("Excellent!")
    elif grade == "B":
        print("Good!")
    elif grade == "C":
        print("Average")
    elif grade == "D":
        print("Below average")
    else:
        print("Failing")
    end
}
'''
        output = self.capture_output(source)
        assert "Good!" in output
        # Ensure only one grade message
        assert output.count("!") == 1
        assert "Excellent!" not in output
        assert "Average" not in output

    def test_boolean_conditions(self):
        """Test elif chains with boolean conditions."""
        source = '''
def main() {
    god flag1 = true
    god flag2 = false
    
    if flag1 and flag2:
        print("Both flags true")
    elif flag1 and not flag2:
        print("Flag1 true, flag2 false")
    elif not flag1 and flag2:
        print("Flag1 false, flag2 true")
    elif not flag1 and not flag2:
        print("Both flags false")
    end
}
'''
        output = self.capture_output(source)
        assert "Flag1 true, flag2 false" in output
        # Ensure only one condition executes
        assert output.count("Flag") == 1

    def test_numeric_comparisons(self):
        """Test elif chains with various numeric comparisons."""
        source = '''
def main() {
    float score = 85.5
    
    if score >= 90:
        print("A grade")
    elif score >= 80:
        print("B grade")
    elif score >= 70:
        print("C grade")
    elif score >= 60:
        print("D grade")
    else:
        print("F grade")
    end
}
'''
        output = self.capture_output(source)
        assert "B grade" in output
        # Ensure only one grade
        assert output.count("grade") == 1

    def test_multiple_elif_clauses(self):
        """Test chains with many elif clauses."""
        source = '''
def main() {
    int day = 3
    
    if day == 1:
        print("Monday")
    elif day == 2:
        print("Tuesday")
    elif day == 3:
        print("Wednesday")
    elif day == 4:
        print("Thursday")
    elif day == 5:
        print("Friday")
    elif day == 6:
        print("Saturday")
    elif day == 7:
        print("Sunday")
    else:
        print("Invalid day")
    end
}
'''
        output = self.capture_output(source)
        assert "Wednesday" in output
        # Ensure only one day is printed
        assert output.count("day") == 1 or output.count("Wednesday") == 1

    def test_elif_with_complex_expressions(self):
        """Test elif with complex expressions."""
        source = '''
def main() {
    int a = 10
    int b = 5
    
    if a + b == 15:
        print("Sum is 15")
    elif a - b == 5:
        print("Difference is 5")
    elif a * b == 50:
        print("Product is 50")
    elif a / b == 2:
        print("Quotient is 2")
    else:
        print("No condition matched")
    end
}
'''
        output = self.capture_output(source)
        assert "Sum is 15" in output
        # Ensure only first matching condition executes
        assert output.count("is") == 1

    def test_elif_without_else(self):
        """Test elif chain without else clause."""
        source = '''
def main() {
    int x = 2
    
    if x == 1:
        print("x is 1")
    elif x == 2:
        print("x is 2")
    elif x == 3:
        print("x is 3")
    end
    
    print("After if chain without else")
}
'''
        output = self.capture_output(source)
        assert "x is 2" in output
        assert "After if chain without else" in output
        # Ensure only one condition executes
        assert output.count("x is") == 1

    def test_nested_elif_chains(self):
        """Test nested elif chains."""
        source = '''
def main() {
    int x = 1
    int y = 2
    
    if x == 1:
        print("Outer: x is 1")
        if y == 1:
            print("Inner: y is 1")
        elif y == 2:
            print("Inner: y is 2")
        elif y == 3:
            print("Inner: y is 3")
        end
    elif x == 2:
        print("Outer: x is 2")
        if y == 1:
            print("Inner: y is 1")
        elif y == 2:
            print("Inner: y is 2")
        end
    end
}
'''
        output = self.capture_output(source)
        assert "Outer: x is 1" in output
        assert "Inner: y is 2" in output
        # Ensure correct nested execution
        assert output.count("Outer:") == 1
        assert output.count("Inner:") == 1

    def test_elif_condition_false_fallthrough(self):
        """Test that false conditions in elif chain don't execute."""
        source = '''
def main() {
    int x = 4
    
    if x == 1:
        print("Condition 1 true")
    elif x == 2:
        print("Condition 2 true")
    elif x == 3:
        print("Condition 3 true")
    elif x == 4:
        print("Condition 4 true")
    elif x == 5:
        print("Condition 5 true")
    else:
        print("No condition true")
    end
}
'''
        output = self.capture_output(source)
        assert "Condition 4 true" in output
        # Ensure only one condition executes
        assert output.count("Condition") == 1

    def test_elif_with_function_calls(self):
        """Test elif chains with function calls in conditions."""
        source = '''
def int get_value() {
    return 42
}

def main() {
    int x = get_value()
    
    if x < 10:
        print("Small value")
    elif x < 50:
        print("Medium value")
    elif x < 100:
        print("Large value")
    else:
        print("Very large value")
    end
}
'''
        output = self.capture_output(source)
        assert "Medium value" in output
        # Ensure only one condition executes
        assert output.count("value") == 1
