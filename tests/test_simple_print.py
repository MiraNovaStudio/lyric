"""
Tests for simple print functionality with indexing operations.
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


class TestSimplePrint:
    """Test simple print functionality with indexing operations."""

    def capture_output(self, source: str) -> str:
        """Capture output from running Lyric source code."""
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        return f.getvalue().strip()

    def test_simple_list_indexing_print(self):
        """Test simple print with list indexing."""
        source = '''
        def main() {
            x = [1, 2, 3]
            print(x[0])
        }
        '''
        
        output = self.capture_output(source)
        assert output == "1"

    def test_list_indexing_multiple_elements(self):
        """Test printing multiple list elements."""
        source = '''
        def main() {
            numbers = [10, 20, 30, 40, 50]
            print(numbers[0])
            print(numbers[1])
            print(numbers[2])
            print(numbers[3])
            print(numbers[4])
        }
        '''
        
        output = self.capture_output(source)
        expected = "10\n20\n30\n40\n50"
        assert output == expected

    def test_list_indexing_with_strings(self):
        """Test list indexing with string elements."""
        source = '''
        def main() {
            fruits = ["apple", "banana", "orange"]
            print("First fruit:", fruits[0])
            print("Second fruit:", fruits[1])
            print("Third fruit:", fruits[2])
        }
        '''
        
        output = self.capture_output(source)
        expected = "First fruit: apple\nSecond fruit: banana\nThird fruit: orange"
        assert output == expected

    def test_list_indexing_mixed_types(self):
        """Test list indexing with mixed data types."""
        source = '''
        def main() {
            mixed = [42, "hello", true, 3.14]
            print("Number:", mixed[0])
            print("String:", mixed[1])
            print("Boolean:", mixed[2])
            print("Float:", mixed[3])
        }
        '''
        
        output = self.capture_output(source)
        expected = "Number: 42\nString: hello\nBoolean: True\nFloat: 3.14"
        assert output == expected

    def test_list_indexing_with_variables(self):
        """Test list indexing using variables."""
        source = '''
        def main() {
            arr = [100, 200, 300]
            index = 1
            print("Value at index", index, ":", arr[index])
        }
        '''
        
        output = self.capture_output(source)
        assert output == "Value at index 1 : 200"
