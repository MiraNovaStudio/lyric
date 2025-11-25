"""
Test suite for arr (list) methods in Lyric (Task 8).

Tests for all arr methods:
- Mutation methods: append, clear, insert, pop, remove, reverse, sort
- Query methods: count, index, copy
- Built-in methods: len, max, min, sum
"""

import pytest
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric, IndexErrorLyric, ValueErrorLyric, TypeErrorLyric


def parse(source: str):
    """Helper to parse source code."""
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse()


def evaluate(ast):
    """Helper to evaluate an AST."""
    interpreter = Interpreter()
    return interpreter.evaluate(ast)


class TestArrMutationMethods:
    """Test arr mutation methods."""

    def test_append_single_element(self):
        """Test append() adds element to the end."""
        code = """
arr numbers = [1, 2, 3]
numbers.append(4)
print numbers[3]
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 4

    def test_append_multiple_times(self):
        """Test multiple append() calls."""
        code = """
arr items = []
items.append(1)
items.append(2)
items.append(3)
print items.len()
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 3

    def test_clear_empties_list(self):
        """Test clear() removes all elements."""
        code = """
arr numbers = [1, 2, 3, 4, 5]
numbers.clear()
print numbers.len()
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 0

    def test_clear_empty_list(self):
        """Test clear() on already empty list."""
        code = """
arr numbers = []
numbers.clear()
print numbers.len()
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 0

    def test_insert_at_beginning(self):
        """Test insert() at index 0."""
        code = """
arr numbers = [2, 3, 4]
numbers.insert(0, 1)
print numbers[0]
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 1

    def test_insert_at_middle(self):
        """Test insert() at middle index."""
        code = """
arr numbers = [1, 3, 4]
numbers.insert(1, 2)
print numbers[1]
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 2

    def test_insert_at_end(self):
        """Test insert() at end index."""
        code = """
arr numbers = [1, 2, 3]
numbers.insert(3, 4)
print numbers[3]
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 4

    def test_pop_default_removes_last(self):
        """Test pop() without index removes last element."""
        code = """
arr numbers = [1, 2, 3, 4]
var last = numbers.pop()
print last
print numbers.len()
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 4, 3

    def test_pop_with_index(self):
        """Test pop() with specific index."""
        code = """
arr numbers = [1, 2, 3, 4]
var second = numbers.pop(1)
print second
print numbers[1]
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 2, 3

    def test_pop_empty_list_raises_error(self):
        """Test pop() on empty list raises IndexError."""
        code = """
arr numbers = []
numbers.pop()
"""
        ast = parse(code)
        with pytest.raises(IndexErrorLyric):
            evaluate(ast)

    def test_remove_first_occurrence(self):
        """Test remove() deletes first occurrence."""
        code = """
arr numbers = [1, 2, 3, 2, 4]
numbers.remove(2)
print numbers[1]
print numbers.len()
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 3, 4

    def test_remove_nonexistent_raises_error(self):
        """Test remove() on nonexistent value raises ValueError."""
        code = """
arr numbers = [1, 2, 3]
numbers.remove(5)
"""
        ast = parse(code)
        with pytest.raises(ValueErrorLyric):
            evaluate(ast)

    def test_reverse_list(self):
        """Test reverse() reverses list in place."""
        code = """
arr numbers = [1, 2, 3, 4, 5]
numbers.reverse()
print numbers[0]
print numbers[4]
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 5, 1

    def test_reverse_empty_list(self):
        """Test reverse() on empty list."""
        code = """
arr numbers = []
numbers.reverse()
print numbers.len()
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 0

    def test_sort_ascending(self):
        """Test sort() sorts in ascending order."""
        code = """
arr numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort()
print numbers[0]
print numbers[7]
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 1, 9

    def test_sort_descending(self):
        """Test sort() with reverse=true sorts descending."""
        code = """
arr numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort(false, true)
print numbers[0]
print numbers[7]
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 9, 1

    def test_sort_strings(self):
        """Test sort() on strings."""
        code = """
arr words = ["dog", "cat", "zebra", "ant"]
words.sort()
print words[0]
print words[3]
"""
        ast = parse(code)
        evaluate(ast)
        # Should print "ant", "zebra"


class TestArrQueryMethods:
    """Test arr query methods."""

    def test_count_single_occurrence(self):
        """Test count() with single occurrence."""
        code = """
arr numbers = [1, 2, 3, 4, 5]
var cnt = numbers.count(3)
print cnt
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 1

    def test_count_multiple_occurrences(self):
        """Test count() with multiple occurrences."""
        code = """
arr numbers = [1, 2, 2, 3, 2, 4]
var cnt = numbers.count(2)
print cnt
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 3

    def test_count_nonexistent(self):
        """Test count() with nonexistent value."""
        code = """
arr numbers = [1, 2, 3]
var cnt = numbers.count(5)
print cnt
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 0

    def test_index_find_first(self):
        """Test index() finds first occurrence."""
        code = """
arr numbers = [1, 2, 3, 2, 4]
var idx = numbers.index(2)
print idx
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 1

    def test_index_with_start(self):
        """Test index() with start parameter."""
        code = """
arr numbers = [1, 2, 3, 2, 4]
var idx = numbers.index(2, 2, 5)
print idx
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 3

    def test_index_not_found_raises_error(self):
        """Test index() raises ValueError when not found."""
        code = """
arr numbers = [1, 2, 3]
numbers.index(5)
"""
        ast = parse(code)
        with pytest.raises(ValueErrorLyric):
            evaluate(ast)

    def test_copy_creates_shallow_copy(self):
        """Test copy() creates a shallow copy."""
        code = """
arr original = [1, 2, 3]
arr copied = original.copy()
copied.append(4)
print original.len()
print copied.len()
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 3, 4


class TestArrBuiltinMethods:
    """Test arr built-in function methods."""

    def test_len_returns_length(self):
        """Test len() returns number of elements."""
        code = """
arr numbers = [1, 2, 3, 4, 5]
print numbers.len()
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 5

    def test_len_empty_list(self):
        """Test len() on empty list."""
        code = """
arr numbers = []
print numbers.len()
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 0

    def test_max_returns_largest(self):
        """Test max() returns largest element."""
        code = """
arr numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print numbers.max()
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 9

    def test_max_empty_raises_error(self):
        """Test max() on empty list raises ValueError."""
        code = """
arr numbers = []
numbers.max()
"""
        ast = parse(code)
        with pytest.raises(ValueErrorLyric):
            evaluate(ast)

    def test_min_returns_smallest(self):
        """Test min() returns smallest element."""
        code = """
arr numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print numbers.min()
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 1

    def test_min_empty_raises_error(self):
        """Test min() on empty list raises ValueError."""
        code = """
arr numbers = []
numbers.min()
"""
        ast = parse(code)
        with pytest.raises(ValueErrorLyric):
            evaluate(ast)

    def test_sum_returns_total(self):
        """Test sum() returns sum of elements."""
        code = """
arr numbers = [1, 2, 3, 4, 5]
print numbers.sum()
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 15

    def test_sum_empty_returns_zero(self):
        """Test sum() on empty list returns 0."""
        code = """
arr numbers = []
print numbers.sum()
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 0

    def test_sum_with_floats(self):
        """Test sum() with floating point numbers."""
        code = """
arr numbers = [1.5, 2.5, 3.0]
print numbers.sum()
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 7.0

    def test_sum_non_numeric_raises_error(self):
        """Test sum() with non-numeric values raises TypeError."""
        code = """
arr mixed = [1, 2, "three"]
mixed.sum()
"""
        ast = parse(code)
        with pytest.raises(TypeErrorLyric):
            evaluate(ast)


class TestArrEdgeCases:
    """Test arr edge cases and error conditions."""

    def test_method_chaining(self):
        """Test chaining multiple method calls."""
        code = """
arr numbers = [3, 1, 4, 1, 5]
numbers.append(2)
numbers.sort()
print numbers[0]
print numbers[5]
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 1, 5

    def test_arr_with_mixed_types(self):
        """Test arr can hold mixed types."""
        code = """
arr mixed = [1, "two", 3.0, true]
print mixed.len()
print mixed[1]
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 4, "two"

    def test_nested_arr(self):
        """Test nested arr (arr of arr)."""
        code = """
arr matrix = [[1, 2], [3, 4]]
print matrix.len()
print matrix[0][1]
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 2, 2

    def test_arr_iteration(self):
        """Test iterating over arr with for loop."""
        code = """
arr numbers = [1, 2, 3]
given item in numbers:
    print item
done
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 1, 2, 3

    def test_arr_slicing_with_methods(self):
        """Test slicing arr and calling methods."""
        code = """
arr numbers = [1, 2, 3, 4, 5]
arr subset = numbers[1:4]
print subset.len()
print subset[0]
"""
        ast = parse(code)
        evaluate(ast)
        # Should print 3, 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
