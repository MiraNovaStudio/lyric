"""
Test suite for the map type (Python dict) in Lyric.

Tests:
- map type declarations and assignments
- Key/value access operations
- Key/value updates
- Iteration over map
- Type compatibility and validation
"""

import pytest
import sys
import io
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import TypeErrorLyric, KeyErrorLyric, RuntimeErrorLyric


def parse(source: str):
    """Helper to parse source code."""
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse()


def evaluate(ast):
    """Helper to evaluate an AST."""
    interpreter = Interpreter()
    return interpreter.evaluate(ast)


class TestMapType:
    """Test the map type in Lyric."""

    def _run_code(self, code: str):
        """Helper function to tokenize, parse, and run code."""
        ast = parse(code)
        return evaluate(ast)

    def test_map_declaration_empty_dict(self):
        """Test map declaration with empty dictionary."""
        code = """
map mydict = {}
print mydict
"""
        result = self._run_code(code)
        # Should print {}

    def test_map_declaration_with_pairs(self):
        """Test map declaration with key-value pairs."""
        code = """
map person = {"name": "Alice", "age": 30, "city": "NYC"}
print person
"""
        result = self._run_code(code)
        # Should print the dictionary

    def test_map_key_access_string_key(self):
        """Test accessing map values with string keys."""
        code = """
map data = {"x": 10, "y": 20}
print data["x"]
print data["y"]
"""
        result = self._run_code(code)
        # Should print 10, 20

    def test_map_key_access_int_key(self):
        """Test accessing map values with integer keys."""
        code = """
map numbers = {1: "one", 2: "two", 3: "three"}
print numbers[1]
print numbers[2]
"""
        result = self._run_code(code)
        # Should print one, two

    def test_map_key_access_missing_key(self):
        """Test accessing non-existent key raises KeyError."""
        code = """
map data = {"a": 1, "b": 2}
print data["c"]
"""
        with pytest.raises(KeyErrorLyric):
            self._run_code(code)

    def test_map_key_assignment_new(self):
        """Test adding new key-value pair to map."""
        code = """
map data = {"x": 10}
data["y"] = 20
print data["y"]
"""
        result = self._run_code(code)
        # Should print 20

    def test_map_key_assignment_update(self):
        """Test updating existing key in map."""
        code = """
map scores = {"alice": 85, "bob": 90}
scores["alice"] = 95
print scores["alice"]
"""
        result = self._run_code(code)
        # Should print 95

    def test_map_mixed_key_types(self):
        """Test map with mixed key types."""
        code = """
map mixed = {"name": "Alice", 1: "first", 2.5: "two-and-half"}
print mixed["name"]
print mixed[1]
print mixed[2.5]
"""
        result = self._run_code(code)
        # Should print Alice, first, two-and-half

    def test_map_mixed_value_types(self):
        """Test map with mixed value types."""
        code = """
map data = {"count": 42, "name": "test", "active": true, "items": [1, 2, 3]}
print data["count"]
print data["name"]
print data["active"]
"""
        result = self._run_code(code)
        # Should print values

    def test_map_nested_dict(self):
        """Test map with nested dictionary structure."""
        code = """
map person = {"name": "Alice", "address": {"city": "NYC", "zip": "10001"}}
print person["name"]
print person["address"]["city"]
"""
        result = self._run_code(code)
        # Should print Alice, NYC

    def test_map_iteration_keys(self):
        """Test iterating over map yields keys."""
        code = """
map data = {"a": 1, "b": 2, "c": 3}
for key in data:
    print key
done
"""
        result = self._run_code(code)
        # Should print a, b, c

    def test_map_type_validation_strict(self):
        """Test map type validation rejects non-dict values."""
        code = """
map mydict = 42
"""
        with pytest.raises(RuntimeErrorLyric):
            self._run_code(code)

    def test_map_type_validation_list(self):
        """Test map type validation rejects list values."""
        code = """
map mydict = [1, 2, 3]
"""
        with pytest.raises(RuntimeErrorLyric):
            self._run_code(code)

    def test_map_type_validation_string(self):
        """Test map type validation rejects string values."""
        code = """
map mydict = "not a dict"
"""
        with pytest.raises(RuntimeErrorLyric):
            self._run_code(code)

    def test_map_empty_dict_iteration(self):
        """Test iterating over empty map."""
        code = """
map empty = {}
for key in empty:
    print key
done
print "done"
"""
        result = self._run_code(code)
        # Should only print "done"

    def test_map_with_list_values(self):
        """Test map containing list values."""
        code = """
map data = {"numbers": [1, 2, 3], "names": ["alice", "bob"]}
print data["numbers"][0]
print data["names"][1]
"""
        result = self._run_code(code)
        # Should print 1, bob

    def test_map_in_function_parameter(self):
        """Test passing map as function parameter."""
        code = """
def print_keys(map data) {
    for key in data:
        print key
    done
}

map mydata = {"x": 1, "y": 2}
print_keys(mydata)
"""
        result = self._run_code(code)
        # Should print x, y

    def test_map_in_function_return(self):
        """Test returning map from function."""
        code = """
map def get_dict() {
    return {"status": "ok", "code": 200}
}

map result = get_dict()
print result["status"]
"""
        result = self._run_code(code)
        # Should print ok

    def test_map_len_builtin(self):
        """Test using len() built-in with map."""
        code = """
map data = {"a": 1, "b": 2, "c": 3}
print len(data)
"""
        result = self._run_code(code)
        # Should print 3

    def test_map_multiple_assignments(self):
        """Test multiple key assignments in sequence."""
        code = """
map config = {}
config["host"] = "localhost"
config["port"] = 8080
config["debug"] = true
print config["host"]
print config["port"]
print config["debug"]
"""
        result = self._run_code(code)
        # Should print localhost, 8080, true

    def test_map_overwrite_value(self):
        """Test overwriting existing values multiple times."""
        code = """
map counter = {"count": 0}
counter["count"] = 1
counter["count"] = 2
counter["count"] = 3
print counter["count"]
"""
        result = self._run_code(code)
        # Should print 3


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

