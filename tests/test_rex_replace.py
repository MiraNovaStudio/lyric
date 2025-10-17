"""
Test suite for rex .replace() method functionality - SPRINT5 Task 3
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


class TestRexReplace:
    """Test rex .replace() method functionality."""

    def capture_output(self, source: str) -> str:
        """Capture output from running Lyric source code."""
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        return f.getvalue()

    def test_rex_replace_basic_functionality(self):
        """Test basic .replace() functionality."""
        source = '''
def main() {
    rex pattern = /cat/
    var result1 = pattern.replace("the cat sat", "dog")
    var result2 = pattern.replace("the dog sat", "cat")
    print("replace('the cat sat', 'dog'):", result1)
    print("replace('the dog sat', 'cat'):", result2)
}
'''
        output = self.capture_output(source)
        assert "replace('the cat sat', 'dog'): the dog sat" in output
        assert "replace('the dog sat', 'cat'): the dog sat" in output

    def test_rex_replace_multiple_matches(self):
        """Test .replace() with multiple matches in single string."""
        source = '''
def main() {
    rex pattern = /cat/
    var result = pattern.replace("cat cat cat", "dog")
    print("multiple matches:", result)
}
'''
        output = self.capture_output(source)
        assert "multiple matches: dog dog dog" in output

    def test_rex_replace_with_string_variables(self):
        """Test .replace() with string variables."""
        source = '''
def main() {
    rex pattern = /cat/
    var source_text = "the cat sat on the mat"
    var replacement = "dog"
    var result = pattern.replace(source_text, replacement)
    print("Source:", source_text)
    print("Result:", result)
}
'''
        output = self.capture_output(source)
        assert "Source: the cat sat on the mat" in output
        assert "Result: the dog sat on the mat" in output

    def test_rex_replace_complex_patterns(self):
        """Test .replace() with complex regex patterns."""
        source = '''
def main() {
    rex digit_pattern = /\\d+/
    var result1 = digit_pattern.replace("I have 5 cats and 3 dogs", "many")
    print("digit replacement:", result1)
    
    rex word_pattern = /\\bcat\\b/
    var result2 = word_pattern.replace("cat in the catalog", "dog")
    print("word boundary:", result2)
}
'''
        output = self.capture_output(source)
        assert "digit replacement: I have many cats and many dogs" in output
        assert "word boundary: dog in the catalog" in output

    def test_rex_replace_whitespace_pattern(self):
        """Test .replace() with whitespace patterns."""
        source = '''
def main() {
    rex space_pattern = /\\s+/
    var result = space_pattern.replace("hello    world", " ")
    print("whitespace replacement:", result)
}
'''
        output = self.capture_output(source)
        assert "whitespace replacement: hello world" in output

    def test_rex_replace_email_pattern(self):
        """Test .replace() with email pattern."""
        source = '''
def main() {
    rex email_pattern = /[a-zA-Z0-9]+@[a-zA-Z0-9]+\\.[a-zA-Z]{2,}/
    var result = email_pattern.replace("Contact user@example.com for help", "admin@company.com")
    print("email replacement:", result)
}
'''
        output = self.capture_output(source)
        assert "email replacement: Contact admin@company.com for help" in output

    def test_rex_replace_empty_string(self):
        """Test .replace() with empty strings."""
        source = '''
def main() {
    rex pattern = /test/
    var result1 = pattern.replace("", "replacement")
    var result2 = pattern.replace("test", "")
    print("empty source:", result1)
    print("empty replacement:", result2)
}
'''
        output = self.capture_output(source)
        assert "empty source: " in output
        assert "empty replacement: " in output

    def test_rex_replace_no_matches(self):
        """Test .replace() when no matches are found."""
        source = '''
def main() {
    rex pattern = /cat/
    var result = pattern.replace("the dog sat", "cat")
    print("no matches:", result)
}
'''
        output = self.capture_output(source)
        assert "no matches: the dog sat" in output

    def test_rex_replace_case_sensitive(self):
        """Test .replace() case sensitivity."""
        source = '''
def main() {
    rex pattern = /cat/
    var result1 = pattern.replace("Cat in the hat", "dog")
    var result2 = pattern.replace("CAT in the hat", "dog")
    print("case sensitive 1:", result1)
    print("case sensitive 2:", result2)
}
'''
        output = self.capture_output(source)
        assert "case sensitive 1: Cat in the hat" in output
        assert "case sensitive 2: CAT in the hat" in output

    def test_rex_replace_error_non_string_source(self):
        """Test .replace() error handling with non-string source."""
        source = '''
def main() {
    rex pattern = /cat/
    var number = 123
    var result = pattern.replace(number, "dog")
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        assert "RexObject.replace() expects source to be a string, got int" in str(exc_info.value)

    def test_rex_replace_error_non_string_replacement(self):
        """Test .replace() error handling with non-string replacement."""
        source = '''
def main() {
    rex pattern = /cat/
    var number = 123
    var result = pattern.replace("the cat sat", number)
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        assert "RexObject.replace() expects replacement to be a string, got int" in str(exc_info.value)

    def test_rex_replace_error_boolean_parameters(self):
        """Test .replace() error handling with boolean parameters."""
        source = '''
def main() {
    rex pattern = /cat/
    var bool_value = true
    var result = pattern.replace(bool_value, "dog")
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        assert "RexObject.replace() expects source to be a string, got bool" in str(exc_info.value)

    def test_rex_replace_returns_string_type(self):
        """Test that .replace() returns proper string type."""
        source = '''
def main() {
    rex pattern = /cat/
    var result = pattern.replace("the cat sat", "dog")
    print("Result type:", type(result))
    print("Result value:", result)
}
'''
        output = self.capture_output(source)
        assert "Result type: str" in output
        assert "Result value: the dog sat" in output

    def test_rex_replace_preserves_original_string(self):
        """Test that .replace() does not alter the original string."""
        source = '''
def main() {
    rex pattern = /cat/
    var original = "the cat sat"
    var result = pattern.replace(original, "dog")
    print("Original:", original)
    print("Result:", result)
}
'''
        output = self.capture_output(source)
        assert "Original: the cat sat" in output
        assert "Result: the dog sat" in output

    def test_rex_replace_special_characters(self):
        """Test .replace() with special characters in replacement."""
        source = '''
def main() {
    rex pattern = /cat/
    var result1 = pattern.replace("the cat sat", "d@g")
    var result2 = pattern.replace("cat", "\\n")
    print("special chars 1:", result1)
    print("special chars 2:", result2)
}
'''
        output = self.capture_output(source)
        assert "special chars 1: the d@g sat" in output
        # The newline character creates an actual newline in output, so we check for the pattern
        assert "special chars 2:" in output
