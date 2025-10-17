"""
Test suite for rex .match() method functionality - SPRINT5 Task 2
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
from lyric.errors import RuntimeErrorLyric


class TestRexMatch:
    """Test rex .match() method functionality."""

    def capture_output(self, source: str) -> str:
        """Capture output from running Lyric source code."""
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        return f.getvalue()

    def test_rex_match_basic_functionality(self):
        """Test basic .match() functionality."""
        source = '''
def main() {
    rex pattern = /^abc/
    var result1 = pattern.match("abcdef")
    var result2 = pattern.match("xyz")
    print("match('abcdef'):", result1)
    print("match('xyz'):", result2)
}
'''
        output = self.capture_output(source)
        assert "match('abcdef'): True" in output
        assert "match('xyz'): False" in output

    def test_rex_match_with_string_variables(self):
        """Test .match() with string variables."""
        source = '''
def main() {
    rex pattern = /^[a-zA-Z]+$/
    var text1 = "hello"
    var text2 = "hello123"
    var result1 = pattern.match(text1)
    var result2 = pattern.match(text2)
    print("match(text1):", result1)
    print("match(text2):", result2)
}
'''
        output = self.capture_output(source)
        assert "match(text1): True" in output
        assert "match(text2): False" in output

    def test_rex_match_complex_patterns(self):
        """Test .match() with complex regex patterns."""
        source = '''
def main() {
    rex email_pattern = /^[a-zA-Z0-9]+@[a-zA-Z0-9]+\\.[a-zA-Z]{2,}$/
    var email1 = "user@example.com"
    var email2 = "invalid-email"
    var result1 = email_pattern.match(email1)
    var result2 = email_pattern.match(email2)
    print("email match 1:", result1)
    print("email match 2:", result2)
}
'''
        output = self.capture_output(source)
        assert "email match 1: True" in output
        assert "email match 2: False" in output

    def test_rex_match_empty_string(self):
        """Test .match() with empty string."""
        source = '''
def main() {
    rex pattern = /^$/
    var result1 = pattern.match("")
    var result2 = pattern.match("not empty")
    print("empty match:", result1)
    print("non-empty match:", result2)
}
'''
        output = self.capture_output(source)
        assert "empty match: True" in output
        assert "non-empty match: False" in output

    def test_rex_match_digit_pattern(self):
        """Test .match() with digit pattern."""
        source = '''
def main() {
    rex pattern = /^\\d+$/
    var result1 = pattern.match("123")
    var result2 = pattern.match("abc")
    var result3 = pattern.match("123abc")
    print("digits only:", result1)
    print("letters only:", result2)
    print("mixed:", result3)
}
'''
        output = self.capture_output(source)
        assert "digits only: True" in output
        assert "letters only: False" in output
        assert "mixed: False" in output

    def test_rex_match_word_boundary(self):
        """Test .match() with word boundary patterns."""
        source = '''
def main() {
    rex pattern = /^\\bword\\b$/
    var result1 = pattern.match("word")
    var result2 = pattern.match("words")
    var result3 = pattern.match("sword")
    print("exact word:", result1)
    print("word with s:", result2)
    print("sword:", result3)
}
'''
        output = self.capture_output(source)
        assert "exact word: True" in output
        assert "word with s: False" in output
        assert "sword: False" in output

    def test_rex_match_whitespace_pattern(self):
        """Test .match() with whitespace patterns."""
        source = '''
def main() {
    rex pattern = /^\\s+$/
    var result1 = pattern.match("   ")
    var result2 = pattern.match("\\t\\n")
    var result3 = pattern.match("hello")
    print("spaces:", result1)
    print("tabs and newlines:", result2)
    print("text:", result3)
}
'''
        output = self.capture_output(source)
        assert "spaces: True" in output
        assert "tabs and newlines: True" in output
        assert "text: False" in output

    def test_rex_match_error_non_string_input(self):
        """Test .match() error handling with non-string input."""
        source = '''
def main() {
    rex pattern = /^abc/
    var number = 123
    var result = pattern.match(number)
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        assert "RexObject.match() expects a string, got int" in str(exc_info.value)

    def test_rex_match_error_boolean_input(self):
        """Test .match() error handling with boolean input."""
        source = '''
def main() {
    rex pattern = /^abc/
    var bool_value = true
    var result = pattern.match(bool_value)
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        assert "RexObject.match() expects a string, got bool" in str(exc_info.value)

    def test_rex_match_multiple_patterns(self):
        """Test .match() with multiple different patterns."""
        source = '''
def main() {
    rex pattern1 = /^[a-z]+$/
    rex pattern2 = /^[A-Z]+$/
    rex pattern3 = /^[0-9]+$/
    
    var text1 = "hello"
    var text2 = "WORLD"
    var text3 = "123"
    
    var result1 = pattern1.match(text1)
    var result2 = pattern2.match(text2)
    var result3 = pattern3.match(text3)
    
    print("lowercase:", result1)
    print("uppercase:", result2)
    print("numbers:", result3)
}
'''
        output = self.capture_output(source)
        assert "lowercase: True" in output
        assert "uppercase: True" in output
        assert "numbers: True" in output

    def test_rex_match_return_boolean_type(self):
        """Test that .match() returns proper boolean type."""
        source = '''
def main() {
    rex pattern = /^test$/
    var result = pattern.match("test")
    print("Result type:", type(result))
    print("Result value:", result)
    
    if result:
        print("Boolean evaluation: True")
    else:
        print("Boolean evaluation: False")
    end
}
'''
        output = self.capture_output(source)
        assert "Result type: bool" in output
        assert "Result value: True" in output
        assert "Boolean evaluation: True" in output
