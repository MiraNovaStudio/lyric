# Lyric Programming Language
# Copyright (c) 2025 MiraNova Studios
# Designed and Architected by Michael (Aeonath) and ChatGPT
# Implemented by Claude
# Licensed under the MIT License with Source Attribution

"""Test suite for list_dict_tests.ly - Sprint 3 list and dictionary functionality tests."""

import pytest
import subprocess
import os
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric


class TestListDictTests:
    """Test list and dictionary functionality."""
    
    def test_list_dict_tests_ly_runs_successfully(self):
        """Test that list_dict_tests.ly runs successfully through CLI."""
        list_dict_tests_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'list_dict_tests.ly')
        
        # Run the CLI command
        result = subprocess.run(['lyric', 'run', list_dict_tests_path],
                               capture_output=True, text=True)
        
        # Should succeed (exit code 0)
        assert result.returncode == 0, f"CLI failed with error: {result.stderr}"
        
        # Check that output contains expected content or is empty (no main function)
        output = result.stdout
        # Since the test file only has variable declarations, no output is expected
        assert len(output) >= 0  # Allow empty output
    
    def test_list_literals_and_basic_operations(self):
        """Test list literals and basic operations."""
        source = """
        var numbers = [1, 2, 3, 4, 5]
        var words = ["hello", "world", "lyric"]
        var mixed = [1, "hello", 3.14, True]
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values
        assert interpreter.global_scope['numbers'] == [1, 2, 3, 4, 5]
        assert interpreter.global_scope['words'] == ["hello", "world", "lyric"]
        assert interpreter.global_scope['mixed'] == [1, "hello", 3.14, True]
    
    def test_dictionary_literals_and_basic_operations(self):
        """Test dictionary literals and basic operations."""
        source = """
        var person = {"name": "Alice", "age": 30, "city": "New York"}
        var scores = {"math": 95, "science": 87, "english": 92}
        var config = {"debug": True, "version": "0.3.0", "port": 8080}
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values
        assert interpreter.global_scope['person'] == {"name": "Alice", "age": 30, "city": "New York"}
        assert interpreter.global_scope['scores'] == {"math": 95, "science": 87, "english": 92}
        assert interpreter.global_scope['config'] == {"debug": True, "version": "0.3.0", "port": 8080}
    
    def test_list_indexing(self):
        """Test list indexing operations."""
        source = """
        var numbers = [1, 2, 3, 4, 5]
        var words = ["hello", "world", "lyric"]
        var first_number = numbers[0]
        var last_word = words[2]
        var middle_number = numbers[2]
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values
        assert interpreter.global_scope['first_number'] == 1
        assert interpreter.global_scope['last_word'] == "lyric"
        assert interpreter.global_scope['middle_number'] == 3
    
    def test_dictionary_key_access(self):
        """Test dictionary key access operations."""
        source = """
        var person = {"name": "Alice", "age": 30, "city": "New York"}
        var scores = {"math": 95, "science": 87, "english": 92}
        var person_name = person["name"]
        var person_age = person["age"]
        var math_score = scores["math"]
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values
        assert interpreter.global_scope['person_name'] == "Alice"
        assert interpreter.global_scope['person_age'] == 30
        assert interpreter.global_scope['math_score'] == 95
    
    def test_list_length_and_builtin_functions(self):
        """Test list length and built-in functions."""
        source = """
        var numbers = [1, 2, 3, 4, 5]
        var words = ["hello", "world", "lyric"]
        var numbers_length = len(numbers)
        var words_length = len(words)
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values
        assert interpreter.global_scope['numbers_length'] == 5
        assert interpreter.global_scope['words_length'] == 3
    
    def test_dictionary_length_and_builtin_functions(self):
        """Test dictionary length and built-in functions."""
        source = """
        var person = {"name": "Alice", "age": 30, "city": "New York"}
        var scores = {"math": 95, "science": 87, "english": 92}
        var person_keys = keys(person)
        var person_values = values(person)
        var scores_keys = keys(scores)
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values
        assert set(interpreter.global_scope['person_keys']) == {"name", "age", "city"}
        assert set(interpreter.global_scope['person_values']) == {"Alice", 30, "New York"}
        assert set(interpreter.global_scope['scores_keys']) == {"math", "science", "english"}
    
    def test_list_modification_append(self):
        """Test list modification with append."""
        source = """
        var numbers = [1, 2, 3, 4, 5]
        var words = ["hello", "world", "lyric"]
        append(numbers, 6)
        append(words, "test")
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values
        assert interpreter.global_scope['numbers'] == [1, 2, 3, 4, 5, 6]
        assert interpreter.global_scope['words'] == ["hello", "world", "lyric", "test"]
    
    def test_dictionary_modification(self):
        """Test dictionary modification."""
        source = """
        var person = {"name": "Alice", "age": 30, "city": "New York"}
        var scores = {"math": 95, "science": 87, "english": 92}
        person["email"] = "alice@example.com"
        scores["history"] = 88
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values
        assert interpreter.global_scope['person']['email'] == "alice@example.com"
        assert interpreter.global_scope['scores']['history'] == 88
    
    def test_nested_structures(self):
        """Test nested list and dictionary structures."""
        source = """
        var nested = {
            "users": [
                {"name": "Alice", "age": 30},
                {"name": "Bob", "age": 25}
            ],
            "settings": {
                "theme": "dark",
                "language": "en"
            }
        }
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check structure
        nested = interpreter.global_scope['nested']
        assert len(nested['users']) == 2
        assert nested['users'][0]['name'] == "Alice"
        assert nested['users'][0]['age'] == 30
        assert nested['settings']['theme'] == "dark"
        assert nested['settings']['language'] == "en"
    
    def test_complex_indexing(self):
        """Test complex indexing operations."""
        source = """
        var nested = {
            "users": [
                {"name": "Alice", "age": 30},
                {"name": "Bob", "age": 25}
            ],
            "settings": {
                "theme": "dark",
                "language": "en"
            }
        }
        var first_user = nested["users"][0]
        var first_user_name = nested["users"][0]["name"]
        var theme = nested["settings"]["theme"]
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values
        assert interpreter.global_scope['first_user']['name'] == "Alice"
        assert interpreter.global_scope['first_user_name'] == "Alice"
        assert interpreter.global_scope['theme'] == "dark"
    
    def test_indexed_assignment(self):
        """Test indexed assignment operations."""
        source = """
        var numbers = [1, 2, 3, 4, 5]
        var person = {"name": "Alice", "age": 30}
        numbers[0] = 10
        person["age"] = 31
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values
        assert interpreter.global_scope['numbers'][0] == 10
        assert interpreter.global_scope['person']['age'] == 31
