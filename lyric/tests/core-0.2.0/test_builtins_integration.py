# Lyric Programming Language
# Copyright (c) 2025 MiraNova Studios
# Developed by Michael (Aeonath), ChatGPT, and Claude
# Licensed under the MIT License with Source Attribution

"""
Test suite for built-in functions integration with interpreter.
"""

import pytest
from lyric.parser import parse
from lyric.interpreter import evaluate


class TestBuiltinsIntegration:
    """Test cases for built-in functions integration."""
    
    def test_print_builtin_available(self):
        """Test that print built-in is available in interpreter."""
        ast = parse('def main() { print("Hello") }')
        interpreter = evaluate(ast)
        # If we get here without error, print is working
        assert True
    
    def test_int_builtin_available(self):
        """Test that int built-in is available in interpreter."""
        ast = parse('def main() { x = int("42") }')
        interpreter = evaluate(ast)
        # If we get here without error, int is working
        assert True
    
    def test_float_builtin_available(self):
        """Test that float built-in is available in interpreter."""
        ast = parse('def main() { x = float("3.14") }')
        interpreter = evaluate(ast)
        # If we get here without error, float is working
        assert True
    
    def test_str_builtin_available(self):
        """Test that str built-in is available in interpreter."""
        ast = parse('def main() { x = str(42) }')
        interpreter = evaluate(ast)
        # If we get here without error, str is working
        assert True
    
    def test_len_builtin_available(self):
        """Test that len built-in is available in interpreter."""
        ast = parse('def main() { x = len("hello") }')
        interpreter = evaluate(ast)
        # If we get here without error, len is working
        assert True
    
    def test_range_builtin_available(self):
        """Test that range built-in is available in interpreter."""
        ast = parse('def main() { given i in range(3): print(i) done }')
        interpreter = evaluate(ast)
        # If we get here without error, range is working
        assert True
    
    def test_all_builtins_registered(self):
        """Test that all built-ins are registered in interpreter."""
        from lyric.interpreter import Interpreter
        interpreter = Interpreter()
        
        # Check that all built-ins are in global scope
        assert 'print' in interpreter.global_scope
        assert 'input' in interpreter.global_scope
        assert 'int' in interpreter.global_scope
        assert 'float' in interpreter.global_scope
        assert 'str' in interpreter.global_scope
        assert 'range' in interpreter.global_scope
        assert 'len' in interpreter.global_scope
        assert 'open' in interpreter.global_scope
        
        # Check that they are callable
        assert callable(interpreter.global_scope['print'])
        assert callable(interpreter.global_scope['input'])
        assert callable(interpreter.global_scope['int'])
        assert callable(interpreter.global_scope['float'])
        assert callable(interpreter.global_scope['str'])
        assert callable(interpreter.global_scope['range'])
        assert callable(interpreter.global_scope['len'])
        assert callable(interpreter.global_scope['open'])
