"""
Tests for list_dict_tests.ly - List and Dictionary functionality.
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


class TestListDictTests:
    """Test list and dictionary functionality from list_dict_tests.ly."""

    def capture_output(self, source: str) -> str:
        """Capture output from running Lyric source code."""
        program = parse(source)
        interpreter = Interpreter()
        
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        return f.getvalue().strip()

    def test_list_dict_tests_execution(self):
        """Test that list_dict_tests.ly runs successfully through CLI."""
        source = '''
        # List and Dictionary Tests
        numbers = [1, 2, 3, 4, 5]
        fruits = ["apple", "banana", "orange"]
        mixed = [1, "hello", true, 3.14]
        empty_list = []
        
        person = {"name": "Alice", "age": 30, "city": "New York"}
        scores = {"math": 95, "science": 87, "english": 92}
        empty_dict = {}
        nested_dict = {"user": {"name": "Bob", "preferences": {"theme": "dark"}}}
        
        def test_list_operations() {
            print("=== List Operations ===")
            print("numbers[0]:", numbers[0])
            print("numbers[2]:", numbers[2])
            print("fruits[1]:", fruits[1])
            print("len(numbers):", len(numbers))
            print("len(fruits):", len(fruits))
            print("len(empty_list):", len(empty_list))
            print("Original numbers:", numbers)
        }
        
        def test_dict_operations() {
            print("=== Dictionary Operations ===")
            print("person['name']:", person["name"])
            print("person['age']:", person["age"])
            print("scores['math']:", scores["math"])
            print("len(person):", len(person))
            print("len(scores):", len(scores))
            print("len(empty_dict):", len(empty_dict))
            print("person keys:", keys(person))
            print("person values:", values(person))
        }
        
        def test_nested_structures() {
            print("=== Nested Structures ===")
            print("mixed[0]:", mixed[0])
            print("mixed[1]:", mixed[1])
            print("mixed[2]:", mixed[2])
            print("mixed[3]:", mixed[3])
            print("nested_dict['user']['name']:", nested_dict["user"]["name"])
            print("nested_dict['user']['preferences']['theme']:", nested_dict["user"]["preferences"]["theme"])
        }
        
        def test_data_structure_types() {
            print("=== Data Structure Types ===")
            print("numbers type:", type(numbers))
            print("fruits type:", type(fruits))
            print("person type:", type(person))
            print("scores type:", type(scores))
            print("mixed type:", type(mixed))
            print("nested_dict type:", type(nested_dict))
        }
        
        def main() {
            print("=== List and Dictionary Tests ===")
            test_list_operations()
            print()
            test_dict_operations()
            print()
            test_nested_structures()
            print()
            test_data_structure_types()
            print("\\n=== List and Dictionary Tests Complete ===")
        }
        '''
        
        output = self.capture_output(source)
        
        # Verify key outputs
        assert "=== List and Dictionary Tests ===" in output
        assert "=== List Operations ===" in output
        assert "numbers[0]: 1" in output
        assert "numbers[2]: 3" in output
        assert "fruits[1]: banana" in output
        assert "len(numbers): 5" in output
        assert "len(fruits): 3" in output
        assert "len(empty_list): 0" in output
        
        assert "=== Dictionary Operations ===" in output
        assert "person['name']: Alice" in output
        assert "person['age']: 30" in output
        assert "scores['math']: 95" in output
        assert "len(person): 3" in output
        assert "len(scores): 3" in output
        assert "len(empty_dict): 0" in output
        
        assert "=== Nested Structures ===" in output
        assert "mixed[0]: 1" in output
        assert "mixed[1]: hello" in output
        assert "mixed[2]: True" in output
        assert "mixed[3]: 3.14" in output
        assert "nested_dict['user']['name']: Bob" in output
        assert "nested_dict['user']['preferences']['theme']: dark" in output
        
        assert "=== Data Structure Types ===" in output
        assert "numbers type: list" in output
        assert "fruits type: list" in output
        assert "person type: dict" in output
        assert "scores type: dict" in output
        assert "mixed type: list" in output
        assert "nested_dict type: dict" in output
        
        assert "=== List and Dictionary Tests Complete ===" in output

    def test_list_indexing_errors(self):
        """Test list indexing error handling."""
        source = '''
        def main() {
            numbers = [1, 2, 3]
            # This should cause an index out of bounds error
            invalid = numbers[10]
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "List index" in error_msg and "out of range" in error_msg

    def test_dict_key_errors(self):
        """Test dictionary key error handling."""
        source = '''
        def main() {
            person = {"name": "Alice", "age": 30}
            # This should cause a key not found error
            invalid = person["nonexistent"]
        }
        '''
        
        program = parse(source)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "not found" in error_msg or "Key" in error_msg
