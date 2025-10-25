# Lyric Programming Language
# Copyright (c) 2025 MiraNova Studios
# Designed and Architected by Michael (Aeonath) and ChatGPT
# Implemented by Claude
# Licensed under the MIT License with Source Attribution

"""Test suite for Sprint 6 Pivot 6.8.2: Regex Literal Syntax Support."""

import pytest
import sys
import os

# Add the lyric module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.ast_nodes import RexNode, TypeDeclarationNode


class TestRegexLiteralSyntax:
    """Test regex literal syntax support."""
    
    def test_basic_regex_literal(self):
        """Test basic regex literal declaration."""
        code = 'rex pattern = /hello/'
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Should create a type declaration with RexNode
        assert len(ast.statements) == 1
        decl_node = ast.statements[0]
        assert isinstance(decl_node, TypeDeclarationNode)
        assert decl_node.name == 'pattern'
        assert decl_node.type_name == 'rex'
        assert isinstance(decl_node.value, RexNode)
        assert decl_node.value.pattern == 'hello'
    
    def test_complex_regex_literal(self):
        """Test complex regex literal with special characters."""
        code = 'rex email = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/'
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Should create a type declaration with RexNode
        assert len(ast.statements) == 1
        decl_node = ast.statements[0]
        assert isinstance(decl_node, TypeDeclarationNode)
        assert decl_node.name == 'email'
        assert decl_node.type_name == 'rex'
        assert isinstance(decl_node.value, RexNode)
        assert 'a-zA-Z0-9._%+-' in decl_node.value.pattern
    
    def test_regex_with_groups(self):
        """Test regex literal with capturing groups."""
        code = 'rex phone = /(\\d{3})-(\\d{3})-(\\d{4})/'
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Should create a type declaration with RexNode
        assert len(ast.statements) == 1
        decl_node = ast.statements[0]
        assert isinstance(decl_node, TypeDeclarationNode)
        assert decl_node.name == 'phone'
        assert decl_node.type_name == 'rex'
        assert isinstance(decl_node.value, RexNode)
        assert '\\d{3}' in decl_node.value.pattern
    
    def test_regex_match_method(self):
        """Test regex match method."""
        code = '''
        rex pattern = /hello/
        var result = pattern.match("hello world")
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        # Check that result is True
        result = interpreter.variables['result']
        assert result is True
    
    def test_regex_search_method(self):
        """Test regex search method."""
        code = '''
        rex pattern = /world/
        var match = pattern.search("hello world")
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        # Check that match is not None
        match = interpreter.variables['match']
        assert match is not None
        assert hasattr(match, 'group')
        assert match.group(0) == 'world'
    
    def test_regex_findall_method(self):
        """Test regex findall method."""
        code = '''
        rex pattern = /\\d+/
        var matches = pattern.findall("I have 5 apples and 10 oranges")
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        # Check that matches contains numbers
        matches = interpreter.variables['matches']
        assert isinstance(matches, list)
        assert '5' in matches
        assert '10' in matches
    
    def test_regex_replace_method(self):
        """Test regex replace method."""
        code = '''
        rex pattern = /\\d+/
        var result = pattern.replace("I have 5 apples", "X")
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        # Check that numbers are replaced
        result = interpreter.variables['result']
        assert isinstance(result, str)
        assert 'X' in result
        assert '5' not in result
    
    def test_regex_group_access(self):
        """Test accessing regex match groups."""
        code = '''
        rex phone = /(\\d{3})-(\\d{3})-(\\d{4})/
        var match = phone.search("Call 555-123-4567")
        var area_code = match.group(1)
        var exchange = match.group(2)
        var number = match.group(3)
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        # Check that groups are extracted correctly
        area_code = interpreter.variables['area_code']
        exchange = interpreter.variables['exchange']
        number = interpreter.variables['number']
        
        assert area_code == '555'
        assert exchange == '123'
        assert number == '4567'
    
    def test_invalid_regex_pattern(self):
        """Test that invalid regex patterns raise errors."""
        code = 'rex invalid = /[unclosed/'
        
        with pytest.raises(Exception):  # Should raise LexError
            tokens = tokenize(code)
    
    def test_regex_in_expression(self):
        """Test regex literal in expressions."""
        code = '''
        rex pattern1 = /hello/
        rex pattern2 = /world/
        var text = "hello world"
        var match1 = pattern1.match(text)
        var match2 = pattern2.search(text)
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        # Check that both patterns work
        match1 = interpreter.variables['match1']
        match2 = interpreter.variables['match2']
        
        assert match1 is True
        assert match2 is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
