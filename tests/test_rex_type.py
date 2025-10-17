"""
Test suite for rex type and regex literal parsing - SPRINT5 Task 1
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
from lyric_lang.errors import LexError, ParseError, RuntimeErrorLyric


class TestRexType:
    """Test rex type and regex literal functionality."""

    def capture_output(self, source: str) -> str:
        """Capture output from running Lyric source code."""
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        return f.getvalue()

    def test_rex_basic_declaration(self):
        """Test basic rex type declaration with regex literal."""
        source = '''
def main() {
    rex pattern = /^abc/
    print("Pattern:", pattern)
    print("Type:", type(pattern))
}
'''
        output = self.capture_output(source)
        assert "Pattern: ^abc" in output
        assert "Type: RexObject" in output

    def test_rex_complex_pattern(self):
        """Test complex regex pattern."""
        source = '''
def main() {
    rex pattern = /[a-zA-Z0-9]+@[a-zA-Z0-9]+\\.[a-zA-Z]{2,}/
    print("Pattern:", pattern)
}
'''
        output = self.capture_output(source)
        assert "Pattern: [a-zA-Z0-9]+@[a-zA-Z0-9]+\\.[a-zA-Z]{2,}" in output

    def test_rex_escaped_characters(self):
        """Test regex with escaped characters."""
        source = '''
def main() {
    rex pattern = /hello\\s+world/
    print("Pattern:", pattern)
}
'''
        output = self.capture_output(source)
        assert "Pattern: hello\\s+world" in output

    def test_rex_empty_pattern(self):
        """Test empty regex pattern."""
        source = '''
def main() {
    rex pattern = //
    print("Pattern:", pattern)
}
'''
        output = self.capture_output(source)
        assert "Pattern:" in output  # Empty pattern should print empty string

    def test_rex_simple_pattern(self):
        """Test simple regex pattern."""
        source = '''
def main() {
    rex pattern = /cat/
    print("Pattern:", pattern)
}
'''
        output = self.capture_output(source)
        assert "Pattern: cat" in output

    def test_rex_type_keyword_recognized(self):
        """Test that rex is recognized as a type keyword."""
        source = '''
def main() {
    rex pattern = /test/
    print("Success: rex keyword recognized")
}
'''
        output = self.capture_output(source)
        assert "Success: rex keyword recognized" in output

    def test_rex_unclosed_literal_error(self):
        """Test that unclosed regex literals raise parse errors."""
        source = '''
def main() {
    rex pattern = /unclosed
    print("Should not reach here")
}
'''
        with pytest.raises(ParseError):
            parse(source, 'test')

    def test_rex_multi_declaration(self):
        """Test multi-variable declaration with rex type."""
        source = '''
def main() {
    rex pattern1, pattern2
    pattern1 = /test/
    pattern2 = /hello/
    print("Pattern1:", pattern1)
    print("Pattern2:", pattern2)
}
'''
        output = self.capture_output(source)
        assert "Pattern1: test" in output
        assert "Pattern2: hello" in output

    def test_rex_function_parameter(self):
        """Test rex type as function parameter."""
        source = '''
def test_regex(rex pattern) {
    print("Pattern:", pattern)
}

def main() {
    test_regex(/hello/)
}
'''
        output = self.capture_output(source)
        assert "Pattern: hello" in output

    def test_rex_function_return_type(self):
        """Test rex type as function return type."""
        source = '''
def rex get_pattern() {
    return /test/
}

def main() {
    rex pattern = get_pattern()
    print("Pattern:", pattern)
}
'''
        output = self.capture_output(source)
        assert "Pattern: test" in output
