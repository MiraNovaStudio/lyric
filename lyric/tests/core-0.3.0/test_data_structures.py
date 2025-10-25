# Lyric Programming Language
# Copyright (c) 2025 MiraNova Studios
# Designed and Architected by Michael (Aeonath) and ChatGPT
# Implemented by Claude
# Licensed under the MIT License with Source Attribution

"""Tests for built-in data structures (lists and dictionaries)."""

import pytest
from lyric.parser import parse
from lyric.interpreter import evaluate
from lyric.errors import RuntimeErrorLyric, ParseError


def test_list_literal_creation():
    """Test creating list literals."""
    source = '''
    def main() {
        list_example = [1, 2, 3]
        return list_example
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == [1, 2, 3]


def test_empty_list_literal():
    """Test creating empty list literals."""
    source = '''
    def main() {
        empty_list = []
        return empty_list
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == []


def test_list_with_mixed_types():
    """Test creating lists with mixed types."""
    source = '''
    def main() {
        mixed_list = [1, "hello", True, 3.14]
        return mixed_list
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == [1, "hello", True, 3.14]


def test_dictionary_literal_creation():
    """Test creating dictionary literals."""
    source = '''
    def main() {
        dict_example = {"key": "value", "number": 42}
        return dict_example
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == {"key": "value", "number": 42}


def test_empty_dictionary_literal():
    """Test creating empty dictionary literals."""
    source = '''
    def main() {
        empty_dict = {}
        return empty_dict
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == {}


def test_dictionary_with_mixed_types():
    """Test creating dictionaries with mixed key and value types."""
    source = '''
    def main() {
        mixed_dict = {"string": 123, 456: "number", "bool": True}
        return mixed_dict
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == {"string": 123, 456: "number", "bool": True}


def test_list_indexing():
    """Test indexing lists."""
    source = '''
    def main() {
        my_list = [10, 20, 30]
        first = my_list[0]
        second = my_list[1]
        third = my_list[2]
        return first + second + third
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 60


def test_dictionary_key_lookup():
    """Test dictionary key lookup."""
    source = '''
    def main() {
        my_dict = {"name": "Alice", "age": 30}
        name = my_dict["name"]
        age = my_dict["age"]
        return name + " is " + str(age)
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == "Alice is 30"


def test_list_index_out_of_range():
    """Test list index out of range error."""
    source = '''
    def main() {
        my_list = [1, 2, 3]
        return my_list[5]
    }'''
    
    ast = parse(source)
    with pytest.raises(RuntimeErrorLyric, match="Index out of range"):
        evaluate(ast)


def test_dictionary_key_not_found():
    """Test dictionary key not found error."""
    source = '''
    def main() {
        my_dict = {"name": "Alice"}
        return my_dict["age"]
    }'''
    
    ast = parse(source)
    with pytest.raises(RuntimeErrorLyric, match="Key not found"):
        evaluate(ast)


def test_list_index_type_error():
    """Test list index type error."""
    source = '''
    def main() {
        my_list = [1, 2, 3]
        return my_list["invalid"]
    }'''
    
    ast = parse(source)
    with pytest.raises(RuntimeErrorLyric, match="Invalid list index"):
        evaluate(ast)


def test_cannot_index_non_indexable():
    """Test indexing non-indexable objects."""
    source = '''
    def main() {
        number = 42
        return number[0]
    }'''
    
    ast = parse(source)
    with pytest.raises(RuntimeErrorLyric, match="Cannot index object"):
        evaluate(ast)


def test_len_function():
    """Test len() function with lists and dictionaries."""
    source = '''
    def main() {
        my_list = [1, 2, 3, 4, 5]
        my_dict = {"a": 1, "b": 2, "c": 3}
        list_len = len(my_list)
        dict_len = len(my_dict)
        return list_len + dict_len
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 8  # 5 + 3


def test_append_function():
    """Test append() function."""
    source = '''
    def main() {
        my_list = [1, 2, 3]
        append(my_list, 4)
        append(my_list, 5)
        return my_list
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == [1, 2, 3, 4, 5]


def test_append_function_type_error():
    """Test append() function type error."""
    source = '''
    def main() {
        not_list = "hello"
        append(not_list, "world")
    }'''
    
    ast = parse(source)
    with pytest.raises(RuntimeErrorLyric, match="append\\(\\) only works on lists"):
        evaluate(ast)


def test_keys_function():
    """Test keys() function."""
    source = '''
    def main() {
        my_dict = {"name": "Alice", "age": 30, "city": "NYC"}
        dict_keys = keys(my_dict)
        return dict_keys
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert set(result) == {"name", "age", "city"}


def test_keys_function_type_error():
    """Test keys() function type error."""
    source = '''
    def main() {
        not_dict = [1, 2, 3]
        return keys(not_dict)
    }'''
    
    ast = parse(source)
    with pytest.raises(RuntimeErrorLyric, match="keys\\(\\) only works on dictionaries"):
        evaluate(ast)


def test_values_function():
    """Test values() function."""
    source = '''
    def main() {
        my_dict = {"a": 1, "b": 2, "c": 3}
        dict_values = values(my_dict)
        return dict_values
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert set(result) == {1, 2, 3}


def test_values_function_type_error():
    """Test values() function type error."""
    source = '''
    def main() {
        not_dict = "hello"
        return values(not_dict)
    }'''
    
    ast = parse(source)
    with pytest.raises(RuntimeErrorLyric, match="values\\(\\) only works on dictionaries"):
        evaluate(ast)


def test_nested_data_structures():
    """Test nested lists and dictionaries."""
    source = '''
    def main() {
        nested = {
            "users": [
                {"name": "Alice", "age": 30},
                {"name": "Bob", "age": 25}
            ],
            "count": 2
        }
        first_user = nested["users"][0]
        first_name = first_user["name"]
        return first_name
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == "Alice"


def test_list_and_dict_in_expressions():
    """Test lists and dictionaries in expressions."""
    source = '''
    def main() {
        numbers = [1, 2, 3]
        info = {"sum": 6, "length": 3}
        total = numbers[0] + numbers[1] + numbers[2]
        expected = info["sum"]
        return total == expected
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == True


def test_dictionary_literal_syntax_errors():
    """Test dictionary literal syntax errors."""
    # Missing colon
    with pytest.raises((ParseError, RuntimeErrorLyric)):
        parse('{"key" "value"}')
    
    # Missing closing brace
    with pytest.raises((ParseError, RuntimeErrorLyric)):
        parse('{"key": "value"')


def test_list_literal_syntax_errors():
    """Test list literal syntax errors."""
    # Missing closing bracket
    with pytest.raises((ParseError, RuntimeErrorLyric)):
        parse('[1, 2, 3')


def test_indexing_syntax_errors():
    """Test indexing syntax errors."""
    # Missing closing bracket
    with pytest.raises((ParseError, RuntimeErrorLyric)):
        parse('my_list[0')


def test_complex_data_structure_operations():
    """Test complex operations with data structures."""
    source = '''
    def main() {
        # Create a list of dictionaries
        people = [
            {"name": "Alice", "scores": [85, 90, 88]},
            {"name": "Bob", "scores": [92, 87, 95]}
        ]
        
        # Get first person's average score
        alice = people[0]
        alice_scores = alice["scores"]
        alice_avg = (alice_scores[0] + alice_scores[1] + alice_scores[2]) / 3
        
        return alice_avg
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 87.66666666666667


def test_data_structure_modification():
    """Test modifying data structures."""
    source = '''
    def main() {
        # Start with empty structures
        numbers = []
        info = {}
        
        # Add items
        append(numbers, 10)
        append(numbers, 20)
        info["count"] = len(numbers)
        info["total"] = numbers[0] + numbers[1]
        
        return info
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == {"count": 2, "total": 30}
