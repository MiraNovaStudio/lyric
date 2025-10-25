# Lyric Programming Language
# Copyright (c) 2025 MiraNova Studios
# Designed and Architected by Michael (Aeonath) and ChatGPT
# Implemented by Claude
# Licensed under the MIT License with Source Attribution

"""Test suite for Sprint 7 Task 1: Regex Match Group Handling."""

import pytest
import sys
import os

# Add the lyric module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.ast_nodes import RexNode, TypeDeclarationNode


class TestRegexGroupHandling:
    """Test regex match group handling functionality."""
    
    def test_simple_regex_pattern_parsing(self):
        """Test that simple regex patterns parse correctly."""
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
    
    def test_regex_pattern_with_groups(self):
        """Test that regex patterns with capture groups parse correctly."""
        code = 'rex title_pattern = /<title>(.*?)<\/title>/'
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Should create a type declaration with RexNode
        assert len(ast.statements) == 1
        decl_node = ast.statements[0]
        assert isinstance(decl_node, TypeDeclarationNode)
        assert decl_node.name == 'title_pattern'
        assert decl_node.type_name == 'rex'
        assert isinstance(decl_node.value, RexNode)
        # The pattern should contain the capture group
        assert '(.*?)' in decl_node.value.pattern
    
    def test_regex_search_returns_match_object(self):
        """Test that regex search returns a match object."""
        code = '''
        rex pattern = /hello/
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
    
    def test_regex_group_access(self):
        """Test accessing regex match groups."""
        code = '''
        rex pattern = /(hello)/
        var match = pattern.search("hello world")
        var group1 = match.group(1)
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        # Check that group1 contains the captured text
        group1 = interpreter.variables['group1']
        assert group1 == 'hello'
    
    def test_regex_group_zero(self):
        """Test accessing group(0) for full match."""
        code = '''
        rex pattern = /(hello)/
        var match = pattern.search("hello world")
        var full_match = match.group(0)
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        # Check that group(0) contains the full match
        full_match = interpreter.variables['full_match']
        assert full_match == 'hello'
    
    def test_regex_group_nonexistent(self):
        """Test that accessing nonexistent group raises error."""
        code = '''
        rex pattern = /(hello)/
        var match = pattern.search("hello world")
        var group2 = match.group(2)
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        
        # This should raise a RuntimeErrorLyric
        with pytest.raises(Exception) as exc_info:
            interpreter.evaluate(ast)
        
        # Check that it's the right error
        assert "group 2 does not exist" in str(exc_info.value)
    
    def test_regex_no_match_handling(self):
        """Test that no match returns None."""
        code = '''
        rex pattern = /goodbye/
        var match = pattern.search("hello world")
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        # Check that match is None
        match = interpreter.variables['match']
        assert match is None
    
    def test_regex_group_on_none_match(self):
        """Test that calling group() on None match raises error."""
        code = '''
        rex pattern = /goodbye/
        var match = pattern.search("hello world")
        var group1 = match.group(1)
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        
        # This should raise an error because match is None
        with pytest.raises(Exception) as exc_info:
            interpreter.evaluate(ast)
        
        # Check that it's the right error
        assert "NoneType" in str(exc_info.value) or "None" in str(exc_info.value)
    
    def test_html_title_extraction(self):
        """Test the specific example from the sprint plan."""
        code = '''
        rex title_pattern = /<title>(.*?)<\/title>/
        var match = title_pattern.search("<title>Hello</title>")
        var title = match.group(1)
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        # Check that title contains the extracted text
        title = interpreter.variables['title']
        assert title == 'Hello'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


