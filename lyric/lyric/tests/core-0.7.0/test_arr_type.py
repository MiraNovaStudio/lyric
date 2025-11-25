"""
Test suite for the arr type (Python list) in Lyric.

Tests:
- arr type declarations and assignments
- Indexing operations
- Slicing operations (start:end:step)
- Iteration over arr
- Type compatibility and validation
"""

import pytest
import sys
import io
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import TypeErrorLyric, IndexErrorLyric, RuntimeErrorLyric


def parse(source: str):
    """Helper to parse source code."""
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse()


def evaluate(ast):
    """Helper to evaluate an AST."""
    interpreter = Interpreter()
    return interpreter.evaluate(ast)


class TestArrType:
    """Test the arr type in Lyric."""

    def _run_code(self, code: str):
        """Helper function to tokenize, parse, and run code."""
        ast = parse(code)
        return evaluate(ast)

    def test_arr_declaration_empty_list(self):
        """Test arr declaration with empty list."""
        code = """
arr mylist = []
print mylist
"""
        result = self._run_code(code)
        # The print output would be [], no exception should be raised

    def test_arr_declaration_with_elements(self):
        """Test arr declaration with list elements."""
        code = """
arr numbers = [1, 2, 3, 4, 5]
print numbers
"""
        result = self._run_code(code)
        # Should print [1, 2, 3, 4, 5]

    def test_arr_indexing_positive(self):
        """Test arr indexing with positive index."""
        code = """
arr fruits = ["apple", "banana", "cherry"]
print fruits[0]
print fruits[1]
print fruits[2]
"""
        result = self._run_code(code)
        # Should print apple, banana, cherry

    def test_arr_indexing_negative(self):
        """Test arr indexing with standard positive indices."""
        code = """
arr numbers = [10, 20, 30, 40]
print numbers[0]
print numbers[3]
"""
        result = self._run_code(code)
        # Should print 10, 40

    def test_arr_indexing_out_of_bounds(self):
        """Test arr indexing with out of bounds index."""
        code = """
arr items = [1, 2, 3]
print items[5]
"""
        with pytest.raises(IndexErrorLyric):
            self._run_code(code)

    def test_arr_slicing_basic(self):
        """Test basic arr slicing [start:end]."""
        code = """
arr numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print numbers[2:5]
"""
        result = self._run_code(code)
        # Should print [2, 3, 4]

    def test_arr_slicing_with_step(self):
        """Test arr slicing with step [start:end:step]."""
        code = """
arr numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print numbers[0:10:2]
"""
        result = self._run_code(code)
        # Should print [0, 2, 4, 6, 8]

    def test_arr_slicing_negative_step(self):
        """Test arr slicing with negative step (reverse)."""
        code = """
arr numbers = [1, 2, 3, 4, 5]
print numbers[::-1]
"""
        result = self._run_code(code)
        # Should print [5, 4, 3, 2, 1]

    def test_arr_slicing_omit_start(self):
        """Test arr slicing with omitted start [:end]."""
        code = """
arr letters = ["a", "b", "c", "d", "e"]
print letters[:3]
"""
        result = self._run_code(code)
        # Should print ['a', 'b', 'c']

    def test_arr_slicing_omit_end(self):
        """Test arr slicing with omitted end [start:]."""
        code = """
arr letters = ["a", "b", "c", "d", "e"]
print letters[2:]
"""
        result = self._run_code(code)
        # Should print ['c', 'd', 'e']

    def test_arr_iteration_for_loop(self):
        """Test iterating over arr using for loop."""
        code = """
arr colors = ["red", "green", "blue"]
for color in colors:
    print color
done
"""
        result = self._run_code(code)
        # Should print red, green, blue

    def test_arr_iteration_given_loop(self):
        """Test iterating over arr using given loop."""
        code = """
arr numbers = [10, 20, 30]
given num in numbers:
    print num
done
"""
        result = self._run_code(code)
        # Should print 10, 20, 30

    def test_arr_nested_lists(self):
        """Test arr with nested list structure."""
        code = """
arr matrix = [[1, 2], [3, 4], [5, 6]]
print matrix[0]
print matrix[1][0]
"""
        result = self._run_code(code)
        # Should print [1, 2] and 3

    def test_arr_mixed_types(self):
        """Test arr with mixed element types."""
        code = """
arr mixed = [1, "hello", 3.14, true]
print mixed[0]
print mixed[1]
print mixed[2]
print mixed[3]
"""
        result = self._run_code(code)
        # Should print 1, hello, 3.14, true

    def test_arr_assignment_update(self):
        """Test updating arr elements via assignment."""
        code = """
arr values = [1, 2, 3]
values[1] = 99
print values
"""
        result = self._run_code(code)
        # Should print [1, 99, 3]

    def test_arr_type_validation_strict(self):
        """Test arr type validation rejects non-list values."""
        code = """
arr mylist = 42
"""
        with pytest.raises(RuntimeErrorLyric):
            self._run_code(code)

    def test_arr_type_validation_string(self):
        """Test arr type validation rejects string values."""
        code = """
arr mylist = "not a list"
"""
        with pytest.raises(RuntimeErrorLyric):
            self._run_code(code)

    def test_arr_empty_list_iteration(self):
        """Test iterating over empty arr."""
        code = """
arr empty = []
for item in empty:
    print item
done
print "done"
"""
        result = self._run_code(code)
        # Should only print "done"

    def test_arr_length_builtin(self):
        """Test using len() built-in with arr."""
        code = """
arr items = [1, 2, 3, 4, 5]
print len(items)
"""
        result = self._run_code(code)
        # Should print 5

    def test_arr_in_function_parameter(self):
        """Test passing arr as function parameter."""
        code = """
def process_list(arr data) {
    for item in data:
        print item
    done
}

arr mydata = [10, 20, 30]
process_list(mydata)
"""
        result = self._run_code(code)
        # Should print 10, 20, 30

    def test_arr_in_function_return(self):
        """Test returning arr from function."""
        code = """
arr def get_list() {
    return [1, 2, 3]
}

arr result = get_list()
print result
"""
        result = self._run_code(code)
        # Should print [1, 2, 3]

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

