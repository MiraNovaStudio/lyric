"""
Test suite for nested scope resolution - SPRINT6 Task 1
"""

import pytest
import sys
import os
import io
from contextlib import redirect_stdout

# Add the parent directory to the path so we can import lyric
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lyric.parser import parse
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric


class TestNestedScopeResolution:
    """Test nested scope resolution, shadowing, and variable destruction."""

    def capture_output(self, source: str) -> str:
        """Capture output from running Lyric source code."""
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        return f.getvalue()

    def test_basic_shadowing(self):
        """Test that inner scope variables shadow outer scope variables."""
        source = '''
def main() {
    var x = "outer"
    print("Outer:", x)
    
    if true:
        var x = "inner"
        print("Inner:", x)
    end
    
    print("After:", x)
}
'''
        output = self.capture_output(source)
        assert "Outer: outer" in output
        assert "Inner: inner" in output
        assert "After: outer" in output

    def test_variable_destruction(self):
        """Test that variables are destroyed when blocks close."""
        source = '''
def main() {
    if true:
        var temp = "temporary"
        print("Inside:", temp)
    end
    
    # This should cause an error
    print("Outside:", temp)
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        assert "Variable 'temp' used before declaration" in str(exc_info.value)

    def test_nested_blocks_shadowing(self):
        """Test shadowing in nested blocks."""
        source = '''
def main() {
    var x = "level1"
    print("Level 1:", x)
    
    if true:
        var x = "level2"
        print("Level 2:", x)
        
        if true:
            var x = "level3"
            print("Level 3:", x)
        end
        
        print("Back to Level 2:", x)
    end
    
    print("Back to Level 1:", x)
}
'''
        output = self.capture_output(source)
        assert "Level 1: level1" in output
        assert "Level 2: level2" in output
        assert "Level 3: level3" in output
        assert "Back to Level 2: level2" in output
        assert "Back to Level 1: level1" in output

    def test_scope_lookup_order(self):
        """Test that variable lookup follows local → enclosing → global order."""
        source = '''
def main() {
    var x = "global"
    var y = "global_y"
    
    if true:
        var x = "local"
        # x should be local, y should be global
        print("x:", x)
        print("y:", y)
    end
}
'''
        output = self.capture_output(source)
        assert "x: local" in output
        assert "y: global_y" in output

    def test_assignment_to_shadowed_variable(self):
        """Test that assignment to a shadowed variable modifies the local one."""
        source = '''
def main() {
    var x = "outer"
    
    if true:
        var x = "inner"
        x = "modified_inner"
        print("Inner modified:", x)
    end
    
    print("Outer unchanged:", x)
}
'''
        output = self.capture_output(source)
        assert "Inner modified: modified_inner" in output
        assert "Outer unchanged: outer" in output

    def test_function_scope_independence(self):
        """Test that function scopes are independent."""
        source = '''
def func1() {
    var x = "func1"
    print("Func1:", x)
}

def func2() {
    var x = "func2"
    print("Func2:", x)
}

def main() {
    var x = "main"
    print("Main:", x)
    func1()
    func2()
    print("Main unchanged:", x)
}
'''
        output = self.capture_output(source)
        assert "Main: main" in output
        assert "Func1: func1" in output
        assert "Func2: func2" in output
        assert "Main unchanged: main" in output

    def test_loop_scope_shadowing(self):
        """Test scope shadowing in loops."""
        source = '''
def main() {
    var x = "outer"
    print("Outer:", x)
    
    given i in range(2):
        var x = "loop"
        print("Loop:", x)
    done
    
    print("After loop:", x)
}
'''
        output = self.capture_output(source)
        assert "Outer: outer" in output
        assert output.count("Loop: loop") == 2
        assert "After loop: outer" in output

    def test_if_else_scope_independence(self):
        """Test that if and else blocks have independent scopes."""
        source = '''
def main() {
    var condition = true
    
    if condition:
        var x = "if_block"
        print("If:", x)
    else:
        var x = "else_block"
        print("Else:", x)
    end
    
    # x should not be accessible here
    print("After:", x)
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        assert "Variable 'x' used before declaration" in str(exc_info.value)

    def test_multiple_variables_shadowing(self):
        """Test shadowing multiple variables in the same block."""
        source = '''
def main() {
    var x = "outer_x"
    var y = "outer_y"
    var z = "outer_z"
    
    if true:
        var x = "inner_x"
        var y = "inner_y"
        # z is not shadowed, should access outer z
        print("x:", x)
        print("y:", y)
        print("z:", z)
    end
    
    print("After - x:", x)
    print("After - y:", y)
    print("After - z:", z)
}
'''
        output = self.capture_output(source)
        assert "x: inner_x" in output
        assert "y: inner_y" in output
        assert "z: outer_z" in output
        assert "After - x: outer_x" in output
        assert "After - y: outer_y" in output
        assert "After - z: outer_z" in output

    def test_type_preservation_in_shadowing(self):
        """Test that type declarations are preserved in shadowing."""
        source = '''
def main() {
    int x = 10
    print("Outer x:", x)
    
    if true:
        str x = "shadowed"
        print("Inner x:", x)
    end
    
    print("After x:", x)
    print("After x type:", type(x))
}
'''
        output = self.capture_output(source)
        assert "Outer x: 10" in output
        assert "Inner x: shadowed" in output
        assert "After x: 10" in output
        assert "After x type: int" in output

    def test_shadowing_with_same_type(self):
        """Test shadowing with the same type."""
        source = '''
def main() {
    int x = 10
    print("Outer x:", x)
    
    if true:
        int x = 20
        print("Inner x:", x)
        x = 30
        print("Modified inner x:", x)
    end
    
    print("After x:", x)
}
'''
        output = self.capture_output(source)
        assert "Outer x: 10" in output
        assert "Inner x: 20" in output
        assert "Modified inner x: 30" in output
        assert "After x: 10" in output

