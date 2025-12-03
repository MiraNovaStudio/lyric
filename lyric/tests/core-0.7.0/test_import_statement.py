# Lyric Programming Language
# Copyright (c) 2025 MiraNova Studios
# Designed and Architected by Michael (Aeonath) and ChatGPT
# Implemented by Claude
# Licensed under the GNU General Public License v3.0

"""def main() {\n    
Test suite for the import statement in Lyric.

Tests importing functions, classes, and module-level variables.
\n}"""

import pytest
import os
import tempfile
import shutil
import io
import sys
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
    """def main() {\n    Helper to evaluate an AST.\n}"""
    interpreter = Interpreter()
    return interpreter.evaluate(ast)


class TestImportStatement:
    """def main() {\n    Test the import statement in Lyric.\n}"""

    def setup_method(self):
        """def main() {\n    Set up test environment with a temporary directory.\n}"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def teardown_method(self):
        """def main() {\n    Clean up temporary directory.\n}"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)

    def _create_module(self, name: str, content: str):
        """def main() {\n    Helper to create a Lyric module file.\n}"""
        with open(f"{name}.ly", 'w') as f:
            f.write(content)

    def _run_code(self, code: str):
        """def main() {\n    Helper function to tokenize, parse, and run code, capturing output.\n}"""
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            ast = parse(code, interactive=True)
            result = evaluate(ast)
            output = sys.stdout.getvalue()
            return result, output
        finally:
            sys.stdout = old_stdout

    def test_import_simple_function(self):
        """def main() {\n    Test importing a module with a simple function.\n}"""
        self._create_module("mathutils", """def main() {\n    
int add(int a, int b) {
    return a + b
}
\n}""")
        
        code = """
import mathutils

def main() {
    int result = add(5, 3)
    print(result)
}
"""
        result, output = self._run_code(code)
        assert "8" in output

    def test_import_module_not_found(self):
        """def main() {\n    Test that importing non-existent module raises error.\n}"""
        code = """
import nonexistent_module

def main() {
    print("done")
}
"""
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            self._run_code(code)
        assert "ModuleNotFoundError" in str(exc_info.value)

    def test_import_function_with_return_value(self):
        """def main() {\n    Test importing function that returns a value.\n}"""
        self._create_module("calculator", """def main() {\n    
int multiply(int a, int b) {
    return a * b
}

int square(int n) {
    return multiply(n, n)
}
\n}""")
        
        code = """
import calculator

def main() {
    int result = square(7)
    print(result)
}
"""
        result, output = self._run_code(code)
        assert "49" in output

    def test_import_preserves_module_scope(self):
        """def main() {\n    Test that functions can access their module's variables.\n}"""
        self._create_module("scoped", """
int local_var = 100

int get_local() {
    return local_var
}
""")
        
        code = """
import scoped

def main() {
    print(get_local())
}
"""
        result, output = self._run_code(code)
        assert "100" in output

    def test_import_function_with_arr(self):
        """def main() {\n    Test that functions work with arr types.\n}"""
        self._create_module("lists", """
int sum_list(arr data) {
    int total = 0
    for item in data:
        total = total + item
    done
    return total
}
""")
        
        code = """
import lists

def main() {
    arr test_data = [10, 20, 30]
    print(sum_list(test_data))
}
"""
        result, output = self._run_code(code)
        assert "60" in output

    def test_import_function_with_map(self):
        """def main() {\n    Test that functions work with map types.\n}"""
        self._create_module("dicts", """def main() {\n    
str get_name(map p) {
    return p["name"]
}
\n}""")
        
        code = """
import dicts

def main() {
    map test_person = {"name": "Bob"}
    print(get_name(test_person))
}
"""
        result, output = self._run_code(code)
        assert "Bob" in output

    def test_import_empty_module(self):
        """def main() {\n    Test importing an empty module.\n}"""
        self._create_module("empty", "")
        
        code = """
import empty

def main() {
    print("imported")
}
"""
        result, output = self._run_code(code)
        assert "imported" in output

    def test_import_module_level_variables(self):
        """def main() {\n    Test that module-level variables can be imported.\n}"""
        # Create a module with variables
        self._create_module("vars_module", """
int MODULE_CONSTANT = 42
str MODULE_NAME = "TestModule"
arr MODULE_LIST = [1, 2, 3]

int get_constant() {
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
        """def main() {\n    Test selective import of variables.\n}"""
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
        """def main() {\n    Test that import all includes module-level variables.\n}"""
        # Create a module with functions, classes, and variables
        self._create_module("full_module", """
int SETTING = 100
str NAME = "FullModule"

int helper() {
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

    def test_import_class(self):
        """def main() {\n    Test importing a class.\n}"""
        self._create_module("classes", """
class Person
    str name
    int age
    
    def Person(str n, int a) {
        self.name = n
        self.age = a
    }
    
    str greet() {
        return "Hello, I'm " + self.name
    }
+++
""")
        
        code = """
import classes

def main() {
    obj p = Person("Alice", 30)
    print(p.name)
    print(p.age)
    print(p.greet())
}
"""
        result, output = self._run_code(code)
        assert "Alice" in output
        assert "30" in output
        assert "Hello, I'm Alice" in output

    def test_selective_import_class(self):
        """def main() {\n    Test selective import of a class.\n}"""
        self._create_module("myclass", """
class Calculator
    int value
    
    def Calculator(int v) {
        self.value = v
    }
    
    int add(int x) {
        return self.value + x
    }
+++

int helper() {
    return 42
}
""")
        
        code = """
import myclass; Calculator

def main() {
    obj calc = Calculator(10)
    print(calc.add(5))
}
"""
        result, output = self._run_code(code)
        assert "15" in output


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
