"""
Test suite for selective imports and 'as' keyword in Lyric.

Tests:
- Selective function imports
- Selective class imports
- 'as' keyword for class aliasing
- Mixed imports (functions and classes)
- Error handling for undefined symbols
"""

import pytest
import os
import tempfile
import shutil
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric


def parse(source: str):
    """Helper to parse source code."""
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse()


def evaluate(ast):
    """Helper to evaluate an AST."""
    interpreter = Interpreter()
    return interpreter.evaluate(ast)


class TestSelectiveImports:
    """Test selective import functionality."""

    def setup_method(self):
        """Set up test environment with a temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def teardown_method(self):
        """Clean up temporary directory."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)

    def _create_module(self, name: str, content: str):
        """Helper to create a Lyric module file."""
        with open(f"{name}.ly", 'w') as f:
            f.write(content)

    def _run_code(self, code: str):
        """Helper function to tokenize, parse, and run code."""
        ast = parse(code)
        return evaluate(ast)

    def test_selective_function_import_single(self):
        """Test importing a single function selectively."""
        self._create_module("mathlib", """
def add(int a, int b) {
    return a + b
}

def subtract(int a, int b) {
    return a - b
}
""")
        
        code = """
import mathlib; add
int result = add(5, 3)
print result
"""
        self._run_code(code)
        # Should print 8, subtract should NOT be imported

    def test_selective_function_import_multiple(self):
        """Test importing multiple functions selectively."""
        self._create_module("mathlib", """
def add(int a, int b) {
    return a + b
}

def multiply(int a, int b) {
    return a * b
}

def divide(int a, int b) {
    return a / b
}
""")
        
        code = """
import mathlib; add, multiply
print add(5, 3)
print multiply(4, 2)
"""
        self._run_code(code)
        # Should print 8, 8. divide should NOT be imported

    def test_selective_class_import(self):
        """Test importing a class selectively."""
        self._create_module("shapes", """
class Circle
    int radius = 0

    def Circle(int r) {
        self.radius = r
    }
+++

class Square
    int side = 0

    def Square(int s) {
        self.side = s
    }
+++
""")
        
        code = """
import shapes; Circle
Circle c = Circle(5)
print c.radius
"""
        self._run_code(code)
        # Should print 5, Square should NOT be imported

    def test_class_import_with_variable_alias(self):
        """Test creating a class alias using variable assignment."""
        self._create_module("mathlib", """
class Calculator
    int value = 0

    def Calculator(int initial) {
        self.value = initial
    }

    def get_sum(int a, int b) {
        return a + b
    }
+++
""")
        
        code = """
import mathlib; Calculator
var calc = Calculator(10)
print calc.value
"""
        self._run_code(code)
        # Should print 10

    def test_mixed_function_and_class_import(self):
        """Test importing both functions and classes selectively."""
        self._create_module("utils", """
def helper(int x) {
    return x * 2
}

class Tool
    int value = 0

    def Tool(int v) {
        self.value = v
    }
+++
""")
        
        code = """
import utils; helper, Tool
print helper(5)
Tool t = Tool(10)
print t.value
"""
        self._run_code(code)
        # Should print 10, 10

    def test_import_undefined_symbol(self):
        """Test importing a symbol that doesn't exist."""
        self._create_module("mathlib", """
def add(int a, int b) {
    return a + b
}
""")
        
        code = """
import mathlib; nonexistent
"""
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            self._run_code(code)
        assert "ImportError" in str(exc_info.value)
        assert "nonexistent" in str(exc_info.value)

    def test_selective_import_multiple_classes(self):
        """Test importing multiple classes selectively."""
        self._create_module("shapes", """
class Circle
    int radius = 0

    def Circle(int r) {
        self.radius = r
    }

    def area() {
        return self.radius * self.radius
    }
+++

class Rectangle
    int width = 0
    int height = 0

    def Rectangle(int w, int h) {
        self.width = w
        self.height = h
    }
+++
""")
        
        code = """
import shapes; Circle, Rectangle
Circle circ = Circle(5)
print circ.area()
"""
        self._run_code(code)

    def test_function_without_as_keyword(self):
        """Test that functions cannot use 'as' keyword (only classes)."""
        self._create_module("mathlib", """
def add(int a, int b) {
    return a + b
}
""")
        
        # Functions should work without 'as' keyword
        code = """
import mathlib; add
print add(5, 3)
"""
        self._run_code(code)

    def test_selective_import_preserves_module_scope(self):
        """Test that selectively imported functions preserve module scope."""
        self._create_module("config", """
int secret = 42

def get_secret() {
    return secret
}

def double_secret() {
    return secret * 2
}
""")
        
        code = """
import config; get_secret
print get_secret()
"""
        self._run_code(code)
        # Should print 42

    def test_all_import_vs_selective_import(self):
        """Test that selective import only imports specified symbols."""
        self._create_module("mathlib", """
def add(int a, int b) {
    return a + b
}

def multiply(int a, int b) {
    return a * b
}
""")
        
        code = """
import mathlib; add
int result = add(5, 3)
print result
"""
        self._run_code(code)
        # multiply should NOT be available

    def test_class_alias_with_as_throws_error(self):
        """Test that using 'as' keyword with classes throws an error."""
        self._create_module("mathlib", """
class Calculator
    int value = 0

    def Calculator(int initial) {
        self.value = initial
    }
+++
""")
        
        code = """
import mathlib; Calculator as calc
"""
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            self._run_code(code)
        assert "ImportError" in str(exc_info.value)
        assert "'as' keyword is not supported for class imports" in str(exc_info.value)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

