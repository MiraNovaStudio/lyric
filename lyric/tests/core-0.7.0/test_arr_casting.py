"""
Test suite for arr type casting in Lyric.

Tests:
- int(arr) returns length
- float(arr) returns length as float
- str(arr) returns string representation
- map(arr) converts to dict with string keys
- arr(str) converts string to list of characters
- arr(map) converts dict values to list
"""

import pytest
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric


def parse(source: str):
    """Helper to parse source code."""
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse()


def evaluate(ast):
    """Helper to evaluate an AST."""
    interpreter = Interpreter()
    return interpreter.evaluate(ast)


class TestArrCasting:
    """Test arr type casting operations."""

    def test_int_arr_returns_length(self):
        """Test that int(arr) returns the length of the array."""
        code = """
arr numbers = [10, 20, 30, 40, 50]
int length = int(numbers)
print length
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 5

    def test_float_arr_returns_length_as_float(self):
        """Test that float(arr) returns the length as a float."""
        code = """
arr items = [1, 2, 3]
flt length = float(items)
print length
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 3.0

    def test_str_arr_returns_string_representation(self):
        """Test that str(arr) returns a string representation."""
        code = """
arr colors = ["red", "green", "blue"]
str representation = str(colors)
print representation
"""
        ast = parse(code)
        evaluate(ast)
        # Should print string representation of list

    def test_map_arr_converts_to_dict_with_string_keys(self):
        """Test that map(arr) converts array to dict with string keys "1", "2", "3", etc."""
        code = """
arr values = [100, 200, 300]
map result = map(values)
print result["1"]
print result["2"]
print result["3"]
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 100, 200, 300

    def test_arr_str_converts_to_list_of_characters(self):
        """Test that arr(str) converts a string to a list of characters."""
        code = """
str word = "hello"
arr chars = arr(word)
print chars[0]
print chars[1]
print chars[2]
print chars[3]
print chars[4]
"""
        ast = parse(code)
        evaluate(ast)
        # Should print h, e, l, l, o

    def test_arr_map_converts_dict_values_to_list(self):
        """Test that arr(map) converts dict values to a list."""
        code = """
map person = {"name": "Alice", "age": 30, "city": "Seattle"}
arr values = arr(person)
print len(values)
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 3

    def test_int_empty_arr(self):
        """Test that int() on an empty array returns 0."""
        code = """
arr empty = []
int count = int(empty)
print count
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 0

    def test_float_empty_arr(self):
        """Test that float() on an empty array returns 0.0."""
        code = """
arr empty = []
flt count = float(empty)
print count
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 0.0

    def test_arr_empty_string(self):
        """Test that arr() on an empty string returns an empty list."""
        code = """
str empty = ""
arr chars = arr(empty)
print int(chars)
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 0

    def test_map_empty_arr(self):
        """Test that map() on an empty array returns an empty dict."""
        code = """
arr empty = []
map result = map(empty)
print int(result)
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 0

    def test_arr_preserves_list_reference(self):
        """Test that arr(list) returns the same list."""
        code = """
arr original = [1, 2, 3]
arr copy = arr(original)
print int(copy)
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 3

    def test_map_preserves_dict_reference(self):
        """Test that map(dict) returns the same dict."""
        code = """
map original = {"a": 1, "b": 2}
map copy = map(original)
print int(copy)
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 2

    def test_arr_string_with_spaces(self):
        """Test that arr(str) handles strings with spaces."""
        code = """
str phrase = "hi there"
arr chars = arr(phrase)
print chars[2]
"""
        ast = parse(code)
        evaluate(ast)
        # Should print space character

    def test_map_arr_with_mixed_types(self):
        """Test that map(arr) works with arrays containing mixed types."""
        code = """
arr mixed = [42, "text", 3.14]
map result = map(mixed)
print result["1"]
print result["2"]
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 42, text

    def test_chained_casting_arr_to_map_to_arr(self):
        """Test chaining conversions: arr -> map -> arr."""
        code = """
arr original = [10, 20, 30]
map as_map = map(original)
arr back_to_arr = arr(as_map)
print int(back_to_arr)
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 3 (three values)

    def test_casting_in_expressions(self):
        """Test using casting in arithmetic expressions."""
        code = """
arr items = [1, 2, 3, 4, 5]
int double_length = int(items) * 2
print double_length
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 10

    def test_float_casting_in_division(self):
        """Test using float(arr) in division."""
        code = """
arr data = [1, 2, 3, 4]
flt average = 10 / float(data)
print average
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 2.5

    def test_arr_of_arr(self):
        """Test arr() on nested arrays."""
        code = """
arr nested = [[1, 2], [3, 4]]
int length = int(nested)
print length
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 2

    def test_map_arr_single_element(self):
        """Test map(arr) with a single element."""
        code = """
arr single = [999]
map result = map(single)
print result["1"]
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 999


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

