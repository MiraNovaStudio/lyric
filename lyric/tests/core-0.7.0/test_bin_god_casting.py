# Lyric Programming Language
# Copyright (c) 2025 MiraNova Studios
# Designed and Architected by Michael (Aeonath) and ChatGPT
# Implemented by Claude
# Licensed under the MIT License with Source Attribution

"""
Test suite for bin() and god() casting functions.
Tests boolean conversion from various types.
"""

import pytest
from lyric.parser import parse
from lyric.interpreter import Interpreter


class TestBinCasting:
    """Test cases for bin() boolean casting function."""
    
    def test_bin_with_nonzero_int(self):
        """Test bin() with non-zero integer returns True."""
        code = """
int x = 5
god result = bin(x)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_bin_with_zero_int(self):
        """Test bin() with zero integer returns False."""
        code = """
int y = 0
god result = bin(y)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_bin_with_negative_int(self):
        """Test bin() with negative integer returns True."""
        code = """
int z = -10
god result = bin(z)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_bin_with_nonzero_float(self):
        """Test bin() with non-zero float returns True."""
        code = """
flt x = 3.14
god result = bin(x)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_bin_with_zero_float(self):
        """Test bin() with zero float returns False."""
        code = """
flt y = 0.0
god result = bin(y)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_bin_with_nonempty_string(self):
        """Test bin() with non-empty string returns True."""
        code = """
str s = "hello"
god result = bin(s)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_bin_with_empty_string(self):
        """Test bin() with empty string returns False."""
        code = """
str s = ""
god result = bin(s)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_bin_with_nonempty_arr(self):
        """Test bin() with non-empty array returns True."""
        code = """
arr items = [1, 2, 3]
god result = bin(items)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_bin_with_empty_arr(self):
        """Test bin() with empty array returns False."""
        code = """
arr items = []
god result = bin(items)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_bin_with_nonempty_map(self):
        """Test bin() with non-empty map returns True."""
        code = """
map data = {"key": "value"}
god result = bin(data)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_bin_with_empty_map(self):
        """Test bin() with empty map returns False."""
        code = """
map data = {}
god result = bin(data)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_bin_with_true(self):
        """Test bin() with True returns True."""
        code = """
god x = True
god result = bin(x)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_bin_with_false(self):
        """Test bin() with False returns False."""
        code = """
god x = False
god result = bin(x)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False


class TestGodCasting:
    """Test cases for god() boolean casting function."""
    
    def test_god_with_nonzero_int(self):
        """Test god() with non-zero integer returns True."""
        code = """
int x = 5
god result = god(x)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_god_with_zero_int(self):
        """Test god() with zero integer returns False."""
        code = """
int y = 0
god result = god(y)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_god_with_negative_int(self):
        """Test god() with negative integer returns True."""
        code = """
int z = -10
god result = god(z)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_god_with_nonzero_float(self):
        """Test god() with non-zero float returns True."""
        code = """
flt x = 3.14
god result = god(x)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_god_with_zero_float(self):
        """Test god() with zero float returns False."""
        code = """
flt y = 0.0
god result = god(y)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_god_with_nonempty_string(self):
        """Test god() with non-empty string returns True."""
        code = """
str s = "hello"
god result = god(s)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_god_with_empty_string(self):
        """Test god() with empty string returns False."""
        code = """
str s = ""
god result = god(s)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_god_with_nonempty_arr(self):
        """Test god() with non-empty array returns True."""
        code = """
arr items = [1, 2, 3]
god result = god(items)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_god_with_empty_arr(self):
        """Test god() with empty array returns False."""
        code = """
arr items = []
god result = god(items)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_god_with_nonempty_map(self):
        """Test god() with non-empty map returns True."""
        code = """
map data = {"key": "value"}
god result = god(data)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_god_with_empty_map(self):
        """Test god() with empty map returns False."""
        code = """
map data = {}
god result = god(data)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_god_with_true(self):
        """Test god() with True returns True."""
        code = """
god x = True
god result = god(x)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_god_with_false(self):
        """Test god() with False returns False."""
        code = """
god x = False
god result = god(x)
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False


