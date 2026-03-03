# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""
Test suite for reserved import names (lyric, lyrical, ly, ly.*).

These names are reserved for the future Lyric standard library (1.2.0).
"""

import pytest
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric


def parse(source: str, interactive: bool = False):
    """Helper to parse source code."""
    tokens = tokenize(source)
    parser = Parser(tokens)
    if interactive:
        parser._interactive_mode = True
        parser.is_top_level = False
    return parser.parse()


def evaluate(ast):
    """Helper to evaluate an AST."""
    interpreter = Interpreter()
    return interpreter.evaluate(ast)


class TestReservedImports:
    def test_import_lyric_reserved(self):
        code = 'import lyric'
        with pytest.raises(RuntimeErrorLyric, match="reserved module name"):
            ast = parse(code)
            evaluate(ast)

    def test_import_lyrical_reserved(self):
        code = 'import lyrical'
        with pytest.raises(RuntimeErrorLyric, match="reserved module name"):
            ast = parse(code)
            evaluate(ast)

    def test_import_ly_reserved(self):
        code = 'import ly'
        with pytest.raises(RuntimeErrorLyric, match="reserved module name"):
            ast = parse(code)
            evaluate(ast)

    def test_error_message_mentions_stdlib(self):
        code = 'import lyric'
        with pytest.raises(RuntimeErrorLyric, match="standard library"):
            ast = parse(code)
            evaluate(ast)
