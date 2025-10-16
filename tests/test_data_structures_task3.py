"""
Tests for Sprint 3 Task 3 - Built-in Data Structures
"""

import pytest
from lyric.parser import parse
from lyric.interpreter import interpret
from lyric.errors import RuntimeErrorLyric


class TestDataStructuresTask3:
    """Test data structures functionality for Task 3."""

    def capture_output(self, program_code):
        """Capture stdout from running a program."""
        import io
        import sys
        from contextlib import redirect_stdout

        # Parse the program code
        program = parse(program_code, "test")

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            interpret(program)
        finally:
            sys.stdout = old_stdout

        return captured_output.getvalue()

    def test_list_literal_creation(self):
        """Test A8: List literals can be created and assigned."""
        source = '''
def main() {
    numbers = [1, 2, 3, 4, 5]
    strings = ["hello", "world", "test"]
    mixed = [1, "hello", 3.14, true]
    
    print("numbers =", numbers)
    print("strings =", strings)
    print("mixed =", mixed)
}
'''
        output = self.capture_output(source)
        assert "numbers = [1, 2, 3, 4, 5]" in output
        assert 'strings = ["hello", "world", "test"]' in output
        assert "mixed = [1, \"hello\", 3.14, True]" in output

    def test_dict_literal_creation(self):
        """Test A9: Dictionary literals can be created and assigned."""
        source = '''
def main() {
    person = {"name": "Alice", "age": 30, "city": "New York"}
    scores = {"math": 95, "english": 87, "science": 92}
    
    print("person =", person)
    print("scores =", scores)
}
'''
        output = self.capture_output(source)
        assert 'person = {name: "Alice", age: 30, city: "New York"}' in output
        assert "scores = {math: 95, english: 87, science: 92}" in output

    def test_list_indexing(self):
        """Test A10: List indexing works correctly."""
        source = '''
def main() {
    numbers = [10, 20, 30, 40, 50]
    
    print("numbers[0] =", numbers[0])
    print("numbers[1] =", numbers[1])
    print("numbers[4] =", numbers[4])
}
'''
        output = self.capture_output(source)
        assert "numbers[0] = 10" in output
        assert "numbers[1] = 20" in output
        assert "numbers[4] = 50" in output

    def test_dict_key_lookup(self):
        """Test A11: Dictionary key lookup works correctly."""
        source = '''
def main() {
    person = {"name": "Alice", "age": 30, "city": "New York"}
    
    print("person['name'] =", person["name"])
    print("person['age'] =", person["age"])
    print("person['city'] =", person["city"])
}
'''
        output = self.capture_output(source)
        assert "person['name'] = Alice" in output
        assert "person['age'] = 30" in output
        assert "person['city'] = New York" in output

    def test_list_index_out_of_bounds_error(self):
        """Test list index out of bounds error."""
        source = '''
def main() {
    numbers = [1, 2, 3]
    print(numbers[5])
}
'''
        program = parse(source, "test")
        
        with pytest.raises(RuntimeErrorLyric, match="List index 5 out of range"):
            interpret(program)

    def test_dict_key_not_found_error(self):
        """Test dictionary key not found error."""
        source = '''
def main() {
    person = {"name": "Alice"}
    print(person["age"])
}
'''
        program = parse(source, "test")
        
        with pytest.raises(RuntimeErrorLyric, match="Key 'age' not found in dictionary"):
            interpret(program)

    def test_append_function(self):
        """Test A12: append() function works correctly."""
        source = '''
def main() {
    numbers = [1, 2, 3]
    print("Before append:", numbers)
    append(numbers, 4)
    print("After append:", numbers)
    append(numbers, "hello")
    print("After append string:", numbers)
}
'''
        output = self.capture_output(source)
        assert "Before append: [1, 2, 3]" in output
        assert "After append: [1, 2, 3, 4]" in output
        assert 'After append string: [1, 2, 3, 4, "hello"]' in output

    def test_keys_function(self):
        """Test A13: keys() function works correctly."""
        source = '''
def main() {
    person = {"name": "Alice", "age": 30, "city": "New York"}
    person_keys = keys(person)
    print("Keys:", person_keys)
}
'''
        output = self.capture_output(source)
        assert 'Keys: ["name", "age", "city"]' in output

    def test_values_function(self):
        """Test A14: values() function works correctly."""
        source = '''
def main() {
    person = {"name": "Alice", "age": 30, "city": "New York"}
    person_values = values(person)
    print("Values:", person_values)
}
'''
        output = self.capture_output(source)
        assert 'Values: ["Alice", 30, "New York"]' in output

    def test_len_function_with_data_structures(self):
        """Test len() function with lists and dictionaries."""
        source = '''
def main() {
    numbers = [1, 2, 3, 4, 5]
    person = {"name": "Alice", "age": 30}
    
    print("Length of numbers:", len(numbers))
    print("Length of person:", len(person))
}
'''
        output = self.capture_output(source)
        assert "Length of numbers: 5" in output
        assert "Length of person: 2" in output

    def test_nested_data_structures(self):
        """Test nested lists and dictionaries."""
        source = '''
def main() {
    # Nested list
    matrix = [[1, 2], [3, 4]]
    print("matrix[0][0] =", matrix[0][0])
    print("matrix[1][1] =", matrix[1][1])
    
    # Nested dictionary (single line to avoid parser issues)
    data = {"user": {"name": "Alice", "age": 30}, "scores": {"math": 95, "english": 87}}
    print("data['user']['name'] =", data["user"]["name"])
    print("data['scores']['math'] =", data["scores"]["math"])
}
'''
        output = self.capture_output(source)
        assert "matrix[0][0] = 1" in output
        assert "matrix[1][1] = 4" in output
        assert "data['user']['name'] = Alice" in output
        assert "data['scores']['math'] = 95" in output

    def test_data_structures_with_expressions(self):
        """Test data structures containing expressions."""
        source = '''
def main() {
    x = 10
    y = 20
    numbers = [x, y, x + y, x * y]
    
    name = "Alice"
    age = 30
    person = {"name": name, "age": age, "double_age": age * 2}
    
    print("numbers =", numbers)
    print("person =", person)
}
'''
        output = self.capture_output(source)
        assert "numbers = [10, 20, 30, 200]" in output
        assert 'person = {name: "Alice", age: 30, double_age: 60}' in output

    def test_empty_data_structures(self):
        """Test empty lists and dictionaries."""
        source = '''
def main() {
    empty_list = []
    empty_dict = {}
    
    print("empty_list =", empty_list)
    print("empty_dict =", empty_dict)
    print("Length of empty_list:", len(empty_list))
    print("Length of empty_dict:", len(empty_dict))
}
'''
        output = self.capture_output(source)
        assert "empty_list = []" in output
        assert "empty_dict = {}" in output
        assert "Length of empty_list: 0" in output
        assert "Length of empty_dict: 0" in output

    def test_comprehensive_data_structures(self):
        """Test comprehensive data structure functionality."""
        source = '''
def main() {
    print("=== Data Structures Test ===")
    
    # Lists
    numbers = [1, 2, 3, 4, 5]
    strings = ["hello", "world", "test"]
    mixed = [1, "hello", 3.14, true, None]
    
    print("numbers =", numbers)
    print("strings =", strings)
    print("mixed =", mixed)
    
    # Dictionaries
    person = {"name": "Alice", "age": 30, "city": "New York"}
    scores = {"math": 95, "english": 87, "science": 92}
    
    print("person =", person)
    print("scores =", scores)
    
    # Indexing
    print("numbers[0] =", numbers[0])
    print("numbers[2] =", numbers[2])
    print("person['name'] =", person["name"])
    print("person['age'] =", person["age"])
    
    # Built-in functions
    append(numbers, 6)
    print("After append:", numbers)
    
    person_keys = keys(person)
    person_values = values(person)
    print("Person keys:", person_keys)
    print("Person values:", person_values)
    
    print("Length of numbers:", len(numbers))
    print("Length of person:", len(person))
    
    print("=== All Data Structure Tests Passed ===")
}
'''
        output = self.capture_output(source)
        assert "=== Data Structures Test ===" in output
        assert "numbers = [1, 2, 3, 4, 5]" in output
        assert 'strings = ["hello", "world", "test"]' in output
        assert "mixed = [1, \"hello\", 3.14, True, None]" in output
        assert 'person = {name: "Alice", age: 30, city: "New York"}' in output
        assert "scores = {math: 95, english: 87, science: 92}" in output
        assert "numbers[0] = 1" in output
        assert "numbers[2] = 3" in output
        assert "person['name'] = Alice" in output
        assert "person['age'] = 30" in output
        assert "After append: [1, 2, 3, 4, 5, 6]" in output
        assert 'Person keys: ["name", "age", "city"]' in output
        assert 'Person values: ["Alice", 30, "New York"]' in output
        assert "Length of numbers: 6" in output
        assert "Length of person: 3" in output
        assert "=== All Data Structure Tests Passed ===" in output
