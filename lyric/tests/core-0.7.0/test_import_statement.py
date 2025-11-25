"""
Test suite for the import statement in Lyric.

Tests:
- Basic module imports
- Importing functions and classes
- Module not found errors
- Circular import detection (if implemented)
- Import path resolution
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


class TestImportStatement:
    """Test the import statement in Lyric."""

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

    def test_import_simple_function(self):
        """Test importing a module with a simple function."""
        # Create a module with a function
        self._create_module("mathutils", """
def add(int a, int b) {
    return a + b
}
""")
        
        # Import and use it
        code = """
import mathutils
int result = add(5, 3)
print result
"""
        self._run_code(code)
        # Should print 8

    def test_import_multiple_functions(self):
        """Test importing a module with multiple functions."""
        self._create_module("helpers", """
def double(int x) {
    return x * 2
}

def triple(int x) {
    return x * 3
}
""")
        
        code = """
import helpers
print double(5)
print triple(5)
"""
        self._run_code(code)
        # Should print 10, 15

    def test_import_with_variables(self):
        """Test importing a module with global variables."""
        self._create_module("config", """
str app_name = "Lyric App"
int version = 1
god debug_mode = true
""")
        
        code = """
import config
print app_name
print version
print debug_mode
"""
        self._run_code(code)
        # Should print values from config

    def test_import_with_class(self):
        """Test importing a module with a class definition."""
        self._create_module("shapes", """
class Circle {
    def Circle(flt radius) {
        self.radius = radius
    }
    
    flt def area() {
        return 3.14159 * self.radius * self.radius
    }
}
""")
        
        code = """
import shapes
var circle = Circle(5.0)
print circle.area()
"""
        self._run_code(code)
        # Should print area

    def test_import_module_not_found(self):
        """Test that importing non-existent module raises error."""
        code = """
import nonexistent_module
"""
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            self._run_code(code)
        assert "ModuleNotFoundError" in str(exc_info.value)
        assert "nonexistent_module" in str(exc_info.value)

    def test_import_function_with_return_value(self):
        """Test importing function that returns a value."""
        self._create_module("calculator", """
int def multiply(int a, int b) {
    return a * b
}

int def square(int n) {
    return multiply(n, n)
}
""")
        
        code = """
import calculator
int result = square(7)
print result
"""
        self._run_code(code)
        # Should print 49

    def test_import_module_with_nested_calls(self):
        """Test importing module where functions call each other."""
        self._create_module("nested", """
int def inner(int x) {
    return x + 10
}

int def outer(int x) {
    return inner(x) * 2
}
""")
        
        code = """
import nested
print outer(5)
"""
        self._run_code(code)
        # Should print 30 (5+10)*2

    def test_import_preserves_module_scope(self):
        """Test that imported module has its own scope during execution."""
        self._create_module("scoped", """
int local_var = 100

int def get_local() {
    return local_var
}
""")
        
        code = """
import scoped
print get_local()
"""
        self._run_code(code)
        # Should print 100

    def test_import_module_with_types(self):
        """Test importing module with typed variables."""
        self._create_module("typed", """
int count = 42
str message = "Hello"
flt pi = 3.14159
""")
        
        code = """
import typed
print count
print message
print pi
"""
        self._run_code(code)
        # Should print all values

    def test_import_error_in_module(self):
        """Test that errors in imported modules are properly reported."""
        self._create_module("broken", """
int x = "not an integer"
""")
        
        code = """
import broken
"""
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            self._run_code(code)
        assert "broken" in str(exc_info.value)

    def test_import_module_with_lists(self):
        """Test importing module with list variables."""
        self._create_module("lists", """
arr numbers = [1, 2, 3, 4, 5]

int def sum_list(arr data) {
    int total = 0
    for item in data:
        total = total + item
    done
    return total
}
""")
        
        code = """
import lists
print sum_list(numbers)
"""
        self._run_code(code)
        # Should print 15

    def test_import_module_with_dicts(self):
        """Test importing module with dictionary variables."""
        self._create_module("dicts", """
map person = {"name": "Alice", "age": 30}

str def get_name(map p) {
    return p["name"]
}
""")
        
        code = """
import dicts
print get_name(person)
"""
        self._run_code(code)
        # Should print Alice

    def test_multiple_imports_same_file(self):
        """Test importing the same module multiple times."""
        self._create_module("utils", """
int def add_one(int x) {
    return x + 1
}
""")
        
        code = """
import utils
print add_one(5)
import utils
print add_one(10)
"""
        self._run_code(code)
        # Should print 6, 11

    def test_import_empty_module(self):
        """Test importing an empty module."""
        self._create_module("empty", "")
        
        code = """
import empty
print "imported"
"""
        self._run_code(code)
        # Should print "imported"

    def test_import_module_with_print(self):
        """Test importing module that has print statements."""
        self._create_module("printer", """
print "Module loading"
str greeting = "Hello from module"
""")
        
        code = """
import printer
print greeting
"""
        self._run_code(code)
        # Should print "Module loading" then "Hello from module"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

