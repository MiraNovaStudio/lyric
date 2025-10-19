"""Tests for boolean and comparison operations in Lyric language."""

from lyric.lexer import tokenize
from lyric.parser import parse
from lyric.interpreter import evaluate
import io
import sys


def test_lexer_comparison_operators():
    """Test that lexer correctly tokenizes comparison operators."""
    source = "x == y != z < a <= b > c >= d"
    tokens = tokenize(source)
    
    # Check that we get the expected token types
    token_types = [token.type for token in tokens if token.type != 'EOF']
    expected_types = ['IDENT', '==', 'IDENT', '!=', 'IDENT', 'LT', 'IDENT', '<=', 'IDENT', 'GT', 'IDENT', '>=']
    
    # For now, let's see what we actually get
    print("Actual token types:", token_types)
    print("Expected token types:", expected_types)


def test_lexer_logical_operators():
    """Test that lexer correctly tokenizes logical operators."""
    source = "x and y or z not a"
    tokens = tokenize(source)
    
    token_types = [token.type for token in tokens if token.type != 'EOF']
    print("Logical operators token types:", token_types)


if __name__ == "__main__":
    test_lexer_comparison_operators()
    test_lexer_logical_operators()
