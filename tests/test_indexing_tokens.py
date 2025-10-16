"""
Tests for tokenization of indexing operations.
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import lyric
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lyric.lexer import tokenize


class TestIndexingTokens:
    """Test tokenization of indexing operations."""

    def test_indexing_tokens(self):
        """Test the tokenization of indexing operations."""
        source = 'y["key"]'
        tokens = tokenize(source, 'test')
        token_types = [t.type for t in tokens]
        
        # Expected token sequence: IDENTIFIER, LBRACKET, STRING, RBRACKET
        expected = ['IDENTIFIER', 'LBRACKET', 'STRING', 'RBRACKET']
        assert token_types == expected
        
        # Verify specific values
        assert tokens[0].value == 'y'
        assert tokens[1].value == '['
        assert tokens[2].value == '"key"'
        assert tokens[3].value == ']'

    def test_list_indexing_tokens(self):
        """Test tokenization of list indexing."""
        source = 'x[0]'
        tokens = tokenize(source, 'test')
        token_types = [t.type for t in tokens]
        
        # Expected token sequence: IDENTIFIER, LBRACKET, INTEGER, RBRACKET
        expected = ['IDENTIFIER', 'LBRACKET', 'INTEGER', 'RBRACKET']
        assert token_types == expected
        
        # Verify specific values
        assert tokens[0].value == 'x'
        assert tokens[1].value == '['
        assert tokens[2].value == '0'
        assert tokens[3].value == ']'

    def test_nested_indexing_tokens(self):
        """Test tokenization of nested indexing."""
        source = 'data["user"]["name"]'
        tokens = tokenize(source, 'test')
        token_types = [t.type for t in tokens]
        
        # Expected token sequence: IDENTIFIER, LBRACKET, STRING, RBRACKET, LBRACKET, STRING, RBRACKET
        expected = ['IDENTIFIER', 'LBRACKET', 'STRING', 'RBRACKET', 'LBRACKET', 'STRING', 'RBRACKET']
        assert token_types == expected
        
        # Verify specific values
        assert tokens[0].value == 'data'
        assert tokens[1].value == '['
        assert tokens[2].value == '"user"'
        assert tokens[3].value == ']'
        assert tokens[4].value == '['
        assert tokens[5].value == '"name"'
        assert tokens[6].value == ']'

    def test_indexing_with_expressions(self):
        """Test tokenization of indexing with expressions."""
        source = 'arr[i + 1]'
        tokens = tokenize(source, 'test')
        token_types = [t.type for t in tokens]
        
        # Expected token sequence: IDENTIFIER, LBRACKET, IDENTIFIER, PLUS, INTEGER, RBRACKET
        expected = ['IDENTIFIER', 'LBRACKET', 'IDENTIFIER', 'PLUS', 'INTEGER', 'RBRACKET']
        assert token_types == expected
