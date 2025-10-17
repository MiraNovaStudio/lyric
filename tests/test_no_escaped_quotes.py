"""
Tests for dictionary operations without escaped quotes.
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


class TestNoEscapedQuotes:
    """Test dictionary operations without escaped quotes."""

    def capture_output(self, source: str) -> str:
        """Capture output from running Lyric source code."""
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        return f.getvalue().strip()

    def test_dict_without_escaped_quotes(self):
        """Test dictionary operations without escaped quotes."""
        source = '''
        def main() {
            y = {"key": "value", "number": 42}
            print("y[key] =", y["key"])
        }
        '''
        
        output = self.capture_output(source)
        assert output == "y[key] = value"

    def test_dict_mixed_types(self):
        """Test dictionary with mixed data types."""
        source = '''
        def main() {
            data = {"name": "Alice", "age": 30, "active": true, "score": 95.5}
            print("Name:", data["name"])
            print("Age:", data["age"])
            print("Active:", data["active"])
            print("Score:", data["score"])
        }
        '''
        
        output = self.capture_output(source)
        expected = "Name: Alice\nAge: 30\nActive: True\nScore: 95.5"
        assert output == expected

    def test_dict_string_keys(self):
        """Test dictionary with various string keys."""
        source = '''
        def main() {
            config = {"host": "localhost", "port": 8080, "debug": false}
            print("Host:", config["host"])
            print("Port:", config["port"])
            print("Debug:", config["debug"])
        }
        '''
        
        output = self.capture_output(source)
        expected = "Host: localhost\nPort: 8080\nDebug: False"
        assert output == expected

    def test_dict_nested_operations(self):
        """Test nested dictionary operations."""
        source = '''
        def main() {
            nested = {"level1": {"level2": {"value": "deep"}}}
            print("Deep value:", nested["level1"]["level2"]["value"])
        }
        '''
        
        output = self.capture_output(source)
        assert output == "Deep value: deep"
