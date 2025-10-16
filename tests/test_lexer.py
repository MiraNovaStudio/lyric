"""
Tests for the lexer module.
"""

import pytest
from lyric.lexer import tokenize, Token, Lexer
from lyric.errors import LexError


class TestLexer:
    """Test cases for the Lyric lexer."""
    
    def test_basic_tokenization(self):
        """Test basic token recognition."""
        source = 'if x > 0:'
        tokens = tokenize(source)
        
        expected = [
            Token('IF', 'if', 1, 1),
            Token('IDENTIFIER', 'x', 1, 4),
            Token('GT', '>', 1, 6),
            Token('INTEGER', '0', 1, 8),
            Token('COLON', ':', 1, 9),
        ]
        
        assert len(tokens) == len(expected)
        for actual, expected_token in zip(tokens, expected):
            assert actual.type == expected_token.type
            assert actual.value == expected_token.value
            assert actual.line == expected_token.line
            assert actual.col == expected_token.col
    
    def test_sample_program_tokenization(self):
        """Test tokenization of the sample program."""
        source = '''if x > 0:
print("positive")
end'''
        
        tokens = tokenize(source)
        
        # Expected sequence: IF, IDENT(x), GT, INT(0), COLON, NEWLINE, 
        # IDENT(print), LPAREN, STRING("positive"), RPAREN, NEWLINE, END
        expected_types = [
            'IF', 'IDENTIFIER', 'GT', 'INTEGER', 'COLON', 'NEWLINE',
            'IDENTIFIER', 'LPAREN', 'STRING', 'RPAREN', 'NEWLINE', 'END'
        ]
        
        actual_types = [token.type for token in tokens]
        assert actual_types == expected_types
        
        # Check specific values
        assert tokens[0].value == 'if'
        assert tokens[1].value == 'x'
        assert tokens[2].value == '>'
        assert tokens[3].value == '0'
        assert tokens[4].value == ':'
        assert tokens[6].value == 'print'
        assert tokens[8].value == '"positive"'
        assert tokens[11].value == 'end'
    
    def test_class_terminator(self):
        """Test class terminator +++ tokenization."""
        source = 'class Player: +++'
        tokens = tokenize(source)
        
        expected_types = ['CLASS', 'IDENTIFIER', 'COLON', 'CLASS_END']
        actual_types = [token.type for token in tokens]
        assert actual_types == expected_types
        
        # Check specific values
        assert tokens[0].value == 'class'
        assert tokens[1].value == 'Player'
        assert tokens[2].value == ':'
        assert tokens[3].value == '+++'
    
    def test_keywords(self):
        """Test all keyword recognition."""
        keywords = ['def', 'class', 'if', 'else', 'given', 'done', 'end', 
                   'try', 'except', 'finally', 'import', 'from', 'as', 'return']
        
        for keyword in keywords:
            tokens = tokenize(keyword)
            assert len(tokens) == 1
            assert tokens[0].type == keyword.upper()
            assert tokens[0].value == keyword
    
    def test_identifiers(self):
        """Test identifier recognition."""
        identifiers = ['x', 'variable', 'my_var', 'var123', '_private', 'CamelCase']
        
        for identifier in identifiers:
            tokens = tokenize(identifier)
            assert len(tokens) == 1
            assert tokens[0].type == 'IDENTIFIER'
            assert tokens[0].value == identifier
    
    def test_numbers(self):
        """Test number tokenization."""
        # Integers
        tokens = tokenize('42')
        assert len(tokens) == 1
        assert tokens[0].type == 'INTEGER'
        assert tokens[0].value == '42'
        
        # Floats
        tokens = tokenize('3.14')
        assert len(tokens) == 1
        assert tokens[0].type == 'FLOAT'
        assert tokens[0].value == '3.14'
    
    def test_strings(self):
        """Test string tokenization."""
        tokens = tokenize('"hello world"')
        assert len(tokens) == 1
        assert tokens[0].type == 'STRING'
        assert tokens[0].value == '"hello world"'
        
        tokens = tokenize('""')
        assert len(tokens) == 1
        assert tokens[0].type == 'STRING'
        assert tokens[0].value == '""'
    
    def test_operators(self):
        """Test operator tokenization."""
        operators = [
            ('+', 'PLUS'),
            ('-', 'MINUS'),
            ('*', 'MULTIPLY'),
            ('/', 'DIVIDE'),
            ('%', 'MODULO'),
            ('=', 'ASSIGN'),
            ('==', 'EQ'),
            ('!=', 'NE'),
            ('<', 'LT'),
            ('>', 'GT'),
            ('<=', 'LE'),
            ('>=', 'GE'),
        ]
        
        for op, expected_type in operators:
            tokens = tokenize(op)
            assert len(tokens) == 1
            assert tokens[0].type == expected_type
            assert tokens[0].value == op
    
    def test_delimiters(self):
        """Test delimiter tokenization."""
        delimiters = [
            ('(', 'LPAREN'),
            (')', 'RPAREN'),
            ('{', 'LBRACE'),
            ('}', 'RBRACE'),
            (':', 'COLON'),
            (',', 'COMMA'),
            (';', 'SEMICOLON'),
            ('.', 'DOT'),
        ]
        
        for delim, expected_type in delimiters:
            tokens = tokenize(delim)
            assert len(tokens) == 1
            assert tokens[0].type == expected_type
            assert tokens[0].value == delim
    
    def test_newlines(self):
        """Test newline handling."""
        source = 'a\nb\nc'
        tokens = tokenize(source)
        
        expected_types = ['IDENTIFIER', 'NEWLINE', 'IDENTIFIER', 'NEWLINE', 'IDENTIFIER']
        actual_types = [token.type for token in tokens]
        assert actual_types == expected_types
    
    def test_whitespace_ignored(self):
        """Test that whitespace is ignored."""
        source = '  if   x   >   0  :  '
        tokens = tokenize(source)
        
        # Should only have non-whitespace tokens
        non_whitespace_tokens = [t for t in tokens if t.type != 'WHITESPACE']
        expected_types = ['IF', 'IDENTIFIER', 'GT', 'INTEGER', 'COLON']
        actual_types = [token.type for token in non_whitespace_tokens]
        assert actual_types == expected_types
    
    def test_comments_ignored(self):
        """Test that comments are ignored."""
        source = 'if x > 0:  # This is a comment\nprint("hello")'
        tokens = tokenize(source)
        
        # Should not have any COMMENT tokens
        comment_tokens = [t for t in tokens if t.type == 'COMMENT']
        assert len(comment_tokens) == 0
        
        # Should have the actual code tokens
        code_tokens = [t for t in tokens if t.type not in ['NEWLINE']]
        expected_types = ['IF', 'IDENTIFIER', 'GT', 'INTEGER', 'COLON', 
                         'IDENTIFIER', 'LPAREN', 'STRING', 'RPAREN']
        actual_types = [token.type for token in code_tokens]
        assert actual_types == expected_types
    
    def test_line_and_column_tracking(self):
        """Test that line and column numbers are correctly tracked."""
        source = '''line1
line2  token
line3'''
        tokens = tokenize(source)
        
        # Find specific tokens
        line1_token = next(t for t in tokens if t.value == 'line1')
        line2_token = next(t for t in tokens if t.value == 'line2')
        token_token = next(t for t in tokens if t.value == 'token')
        line3_token = next(t for t in tokens if t.value == 'line3')
        
        assert line1_token.line == 1 and line1_token.col == 1
        assert line2_token.line == 2 and line2_token.col == 1
        assert token_token.line == 2 and token_token.col == 8  # After "line2  "
        assert line3_token.line == 3 and line3_token.col == 1
    
    def test_complex_program(self):
        """Test tokenization of a complex program."""
        source = '''def main() {
    if x > 0:
        print("positive")
    else:
        print("negative")
    end
}'''
        
        tokens = tokenize(source)
        token_types = [t.type for t in tokens if t.type != 'NEWLINE']
        
        expected = [
            'DEF', 'IDENTIFIER', 'LPAREN', 'RPAREN', 'LBRACE',
            'IF', 'IDENTIFIER', 'GT', 'INTEGER', 'COLON',
            'IDENTIFIER', 'LPAREN', 'STRING', 'RPAREN',
            'ELSE', 'COLON',
            'IDENTIFIER', 'LPAREN', 'STRING', 'RPAREN',
            'END',
            'RBRACE'
        ]
        
        assert token_types == expected
    
    def test_error_handling(self):
        """Test error handling for invalid characters."""
        source = 'x @ y'  # @ is not a valid token
        
        with pytest.raises(LexError) as exc_info:
            tokenize(source)
        
        assert "Unexpected character '@'" in str(exc_info.value)
    
    def test_empty_source(self):
        """Test tokenization of empty source."""
        tokens = tokenize('')
        assert len(tokens) == 0
    
    def test_whitespace_only(self):
        """Test tokenization of whitespace-only source."""
        tokens = tokenize('   \t  \n  \t  ')
        # Should have no tokens except newlines
        non_newline_tokens = [t for t in tokens if t.type != 'NEWLINE']
        assert len(non_newline_tokens) == 0
    
    def test_comment_only(self):
        """Test tokenization of comment-only source."""
        tokens = tokenize('# This is just a comment')
        # Should have no tokens
        assert len(tokens) == 0
