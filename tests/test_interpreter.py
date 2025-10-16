"""
Tests for the Lyric interpreter.
"""

import pytest
import io
import sys
from lyric.parser import parse
from lyric.interpreter import interpret


class TestInterpreter:
    """Test cases for the interpreter."""
    
    def capture_output(self, program_code):
        """Capture stdout from running a program."""
        # Parse the program
        program = parse(program_code)
        
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        
        try:
            # Run the program
            interpret(program)
            
            # Get the output
            output = buffer.getvalue().strip()
            return output
        finally:
            sys.stdout = old_stdout
    
    def test_hello_example(self):
        """Test the hello.ly example."""
        source = '''def main() {
	print("Hello, Lyric!")
}'''
        output = self.capture_output(source)
        assert output == "Hello, Lyric!"
    
    def test_if_demo_example(self):
        """Test the if_demo.ly example."""
        source = '''def main() {
	x = 5
	if x > 0:
		print("positive")
	else:
		print("non-positive")
	end
}'''
        output = self.capture_output(source)
        assert output == "positive"
    
    def test_loop_example(self):
        """Test the loop.ly example."""
        source = '''def main() {
	given i in range(3):
		print(i)
	done
}'''
        output = self.capture_output(source)
        expected = "0\n1\n2"
        assert output == expected
    
    def test_class_example(self):
        """Test a class definition example."""
        source = '''class Player:
	name = "Guest"
	def greet() {
		print("Hello,", self.name)
	}
	+++'''
        
        # This should parse without errors
        program = parse(source)
        assert len(program.statements) == 1
        assert program.statements[0].name == "Player"
    
    def test_function_with_parameters(self):
        """Test function with parameters."""
        source = '''def add(a, b) {
	return a + b
}

def main() {
	result = add(5, 3)
	print(result)
}'''
        output = self.capture_output(source)
        assert output == "8"
    
    def test_multiple_elif(self):
        """Test multiple elif clauses."""
        source = '''def main() {
	x = 2
	if x == 1:
		print("one")
	else if x == 2:
		print("two")
	else if x == 3:
		print("three")
	else:
		print("other")
	end
}'''
        output = self.capture_output(source)
        assert output == "two"
    
    def test_while_loop(self):
        """Test while-style loop."""
        source = '''def main() {
	x = 3
	given x > 0:
		print(x)
		x = x - 1
	done
}'''
        output = self.capture_output(source)
        expected = "3\n2\n1"
        assert output == expected
    
    def test_variable_scoping(self):
        """Test variable scoping."""
        source = '''def test_scope() {
	x = "local"
	print(x)
}

def main() {
	x = "global"
	test_scope()
	print(x)
}'''
        output = self.capture_output(source)
        expected = "local\nglobal"
        assert output == expected
    
    def test_builtin_functions(self):
        """Test built-in function integration."""
        source = '''def main() {
	print("Testing built-ins:")
	num = int("42")
	float_num = float("3.14")
	str_val = str(123)
	print("int:", num, "float:", float_num, "str:", str_val)
	length = len("hello")
	print("len of 'hello':", length)
}'''
        output = self.capture_output(source)
        expected = "Testing built-ins:\nint: 42 float: 3.14 str: 123\nlen of 'hello': 5"
        assert output == expected
    
    def test_arithmetic_expressions(self):
        """Test arithmetic expression evaluation."""
        source = '''def main() {
	x = 10 + 5 * 2
	print("Result:", x)
	y = (10 + 5) * 2
	print("Parentheses:", y)
}'''
        output = self.capture_output(source)
        expected = "Result: 20\nParentheses: 30"
        assert output == expected