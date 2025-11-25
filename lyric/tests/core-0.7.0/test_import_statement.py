"""
Test suite for the import statement in Lyric.

Tests that only functions and classes are imported (NOT variables).
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
        self._create_module("mathutils", """
def add(int a, int b) {
    return a + b
}
""")
        
        code = """
import mathutils
int result = add(5, 3)
print result
"""
        self._run_code(code)

    def test_import_rejects_variables(self):
        """Test that variables are NOT imported from modules."""
        self._create_module("config", """
str app_name = "Lyric App"
""")
        
        code = """
import config
print app_name
"""
        # Variables should NOT be imported, so this should raise an error
        with pytest.raises(RuntimeErrorLyric):
            self._run_code(code)

    def test_import_module_not_found(self):
        """Test that importing non-existent module raises error."""
        code = """
import nonexistent_module
"""
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            self._run_code(code)
        assert "ModuleNotFoundError" in str(exc_info.value)

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

    def test_import_preserves_module_scope(self):
        """Test that functions can access their module's variables."""
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

    def test_import_function_with_arr(self):
        """Test that functions work with arr types."""
        self._create_module("lists", """
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
arr test_data = [10, 20, 30]
print sum_list(test_data)
"""
        self._run_code(code)

    def test_import_function_with_map(self):
        """Test that functions work with map types."""
        self._create_module("dicts", """
str def get_name(map p) {
    return p["name"]
}
""")
        
        code = """
import dicts
map test_person = {"name": "Bob"}
print get_name(test_person)
"""
        self._run_code(code)

    def test_import_empty_module(self):
        """Test importing an empty module."""
        self._create_module("empty", "")
        
        code = """
import empty
print "imported"
"""
        self._run_code(code)

    def test_import_module_with_print(self):
        """Test importing module that executes code."""
        self._create_module("printer", """
print "Module loading"

def greet() {
    print "Hello from module"
}
""")
        
        code = """
import printer
greet()
"""
        self._run_code(code)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


    def test_import_module_level_variables(self):
        """Test that module-level variables can be imported."""
        # Create a module with variables
        self._create_module("vars_module", """
int MODULE_CONSTANT = 42
str MODULE_NAME = "TestModule"
arr MODULE_LIST = [1, 2, 3]

def get_constant() {
    return MODULE_CONSTANT
}
""")
        
        # Import and use the variables
        code = """
import vars_module

def main() {
    print(MODULE_CONSTANT)
    print(MODULE_NAME)
    print(MODULE_LIST[0])
    print(get_constant())
}
"""
        result, output = self._run_code(code)
        assert "42" in output
        assert "TestModule" in output
        assert "1" in output

    def test_selective_import_with_variables(self):
        """Test selective import of variables."""
        # Create a module
        self._create_module("mixed_module", """
int VALUE_A = 10
int VALUE_B = 20
int VALUE_C = 30

int add(int x, int y) {
    return x + y
}
""")
        
        # Selective import of variables
        code = """
import mixed_module; VALUE_A, VALUE_B, add

def main() {
    print(VALUE_A)
    print(VALUE_B)
    print(add(VALUE_A, VALUE_B))
}
"""
        result, output = self._run_code(code)
        assert "10" in output
        assert "20" in output
        assert "30" in output  # 10 + 20

    def test_import_all_includes_variables(self):
        """Test that import all includes module-level variables."""
        # Create a module with functions, classes, and variables
        self._create_module("full_module", """
int SETTING = 100
str NAME = "FullModule"

def helper() {
    return SETTING * 2
}

class Config
    int value
    
    def Config() {
        self.value = SETTING
    }
+++
""")
        
        # Import all
        code = """
import full_module

def main() {
    print(SETTING)
    print(NAME)
    print(helper())
    obj cfg = Config()
    print(cfg.value)
}
"""
        result, output = self._run_code(code)
        assert "100" in output
        assert "FullModule" in output
        assert "200" in output  # helper() returns SETTING * 2
