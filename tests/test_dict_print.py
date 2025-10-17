"""
Tests for dictionary indexing and printing functionality.
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


class TestDictPrint:
    """Test dictionary indexing and printing functionality."""

    def capture_output(self, source: str) -> str:
        """Capture output from running Lyric source code."""
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        return f.getvalue().strip()

    def test_dict_print_functionality(self):
        """Test print with dictionary indexing."""
        source = '''
        def main() {
            y = {"key": "value"}
            print(y["key"])
        }
        '''
        
        output = self.capture_output(source)
        assert output == "value"

    def test_dict_print_with_multiple_keys(self):
        """Test dictionary indexing with multiple keys."""
        source = '''
        def main() {
            person = {"name": "Alice", "age": 30, "city": "New York"}
            print(person["name"])
            print(person["age"])
            print(person["city"])
        }
        '''
        
        output = self.capture_output(source)
        expected = "Alice\n30\nNew York"
        assert output == expected

    def test_dict_print_nested(self):
        """Test nested dictionary indexing."""
        source = '''
        def main() {
            data = {"user": {"name": "Bob", "preferences": {"theme": "dark"}}}
            print(data["user"]["name"])
            print(data["user"]["preferences"]["theme"])
        }
        '''
        
        output = self.capture_output(source)
        expected = "Bob\ndark"
        assert output == expected
