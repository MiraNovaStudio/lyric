"""
Test suite for try/catch/finally/fade syntax - SPRINT6 Task 3
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


class TestTryCatchFinallyFade:
    """Test try/catch/finally/fade syntax implementation."""

    def capture_output(self, source: str) -> str:
        """Capture output from running Lyric source code."""
        program = parse(source, 'test')
        interpreter = Interpreter()
        
        f = io.StringIO()
        with redirect_stdout(f):
            interpreter.interpret(program)
        
        return f.getvalue()

    def test_try_catch_finally_basic_success(self):
        """Test try block with no errors, catch and finally present."""
        source = '''
def main() {
    try:
        print("In try block")
        int x = 42
        print("x =", x)
    catch:
        print("In catch block")
    finally:
        print("In finally block")
    fade
    
    print("After try/catch/finally")
}
'''
        output = self.capture_output(source)
        assert "In try block" in output
        assert "x = 42" in output
        assert "In finally block" in output
        assert "After try/catch/finally" in output
        # Catch block should not execute
        assert output.count("In catch block") == 0

    def test_try_catch_finally_basic_error(self):
        """Test try block with error, caught by catch block."""
        source = '''
def main() {
    try:
        print("In try block")
        int x = 42
        x = "error"  # Type error
    catch:
        print("In catch block - error caught!")
    finally:
        print("In finally block")
    fade
    
    print("After try/catch/finally")
}
'''
        output = self.capture_output(source)
        assert "In try block" in output
        assert "In catch block - error caught!" in output
        assert "In finally block" in output
        assert "After try/catch/finally" in output

    def test_try_catch_only_no_error(self):
        """Test try block with only catch, no finally, no error."""
        source = '''
def main() {
    try:
        print("In try block")
        int x = 42
        print("x =", x)
    catch:
        print("In catch block")
    fade
    
    print("After try/catch")
}
'''
        output = self.capture_output(source)
        assert "In try block" in output
        assert "x = 42" in output
        assert "After try/catch" in output
        # Catch block should not execute
        assert output.count("In catch block") == 0

    def test_try_catch_only_with_error(self):
        """Test try block with only catch, no finally, with error."""
        source = '''
def main() {
    try:
        print("In try block")
        int x = 42
        x = "error"  # Type error
    catch:
        print("In catch block - error caught!")
    fade
    
    print("After try/catch")
}
'''
        output = self.capture_output(source)
        assert "In try block" in output
        assert "In catch block - error caught!" in output
        assert "After try/catch" in output

    def test_try_finally_only_no_error(self):
        """Test try block with only finally, no catch, no error."""
        source = '''
def main() {
    try:
        print("In try block")
        int x = 42
        print("x =", x)
    finally:
        print("In finally block")
    fade
    
    print("After try/finally")
}
'''
        output = self.capture_output(source)
        assert "In try block" in output
        assert "x = 42" in output
        assert "In finally block" in output
        assert "After try/finally" in output

    def test_try_finally_only_with_error(self):
        """Test try block with only finally, no catch, with error."""
        source = '''
def main() {
    try:
        print("In try block")
        int x = 42
        x = "error"  # Type error
    finally:
        print("In finally block")
    fade
    
    print("After try/finally")
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'x'" in error_msg
        assert "expected int" in error_msg
        assert "got str" in error_msg

    def test_nested_try_blocks(self):
        """Test nested try/catch/finally blocks."""
        source = '''
def main() {
    try:
        print("In outer try block")
        try:
            print("  In inner try block")
            int y = 10
            y = "error"  # Type error
        catch:
            print("  In inner catch block - error caught!")
        finally:
            print("  In inner finally block")
        fade
        print("In outer try block after inner block")
    catch:
        print("In outer catch block")
    finally:
        print("In outer finally block")
    fade
    
    print("After nested try blocks")
}
'''
        output = self.capture_output(source)
        assert "In outer try block" in output
        assert "In inner try block" in output
        assert "In inner catch block - error caught!" in output
        assert "In inner finally block" in output
        assert "In outer try block after inner block" in output
        assert "In outer finally block" in output
        assert "After nested try blocks" in output
        # Outer catch should not execute
        assert output.count("In outer catch block") == 0

    def test_error_in_catch_block(self):
        """Test error occurring in catch block."""
        source = '''
def main() {
    try:
        print("In try block")
        int x = 42
        x = "error"  # Type error
    catch:
        print("In catch block")
        int y = 10
        y = "another error"  # Another type error
    finally:
        print("In finally block")
    fade
    
    print("After try/catch/finally")
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'y'" in error_msg
        assert "expected int" in error_msg
        assert "got str" in error_msg

    def test_error_in_finally_block(self):
        """Test error occurring in finally block."""
        source = '''
def main() {
    try:
        print("In try block")
        int x = 42
        x = "error"  # Type error
    catch:
        print("In catch block - error caught!")
    finally:
        print("In finally block")
        int z = 10
        z = "finally error"  # Error in finally
    fade
    
    print("After try/catch/finally")
}
'''
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            program = parse(source, 'test')
            interpreter = Interpreter()
            interpreter.interpret(program)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch for variable 'z'" in error_msg
        assert "expected int" in error_msg
        assert "got str" in error_msg

    def test_fade_required_terminator(self):
        """Test that fade is required to close try/catch/finally blocks."""
        source = '''
def main() {
    try:
        print("In try block")
    catch:
        print("In catch block")
    finally:
        print("In finally block")
    # Missing fade - should cause parse error
}
'''
        with pytest.raises(Exception):  # Should be a parse error
            parse(source, 'test')

    def test_try_block_without_catch_or_finally(self):
        """Test try block without catch or finally (should be valid but not useful)."""
        source = '''
def main() {
    try:
        print("In try block")
        int x = 42
        print("x =", x)
    fade
    
    print("After try block")
}
'''
        output = self.capture_output(source)
        assert "In try block" in output
        assert "x = 42" in output
        assert "After try block" in output

    def test_multiple_try_blocks_in_sequence(self):
        """Test multiple try/catch/finally blocks in sequence."""
        source = '''
def main() {
    print("=== First try block ===")
    try:
        print("In first try block")
        int x = 42
        x = "error"  # Type error
    catch:
        print("In first catch block - error caught!")
    finally:
        print("In first finally block")
    fade
    
    print("=== Second try block ===")
    try:
        print("In second try block")
        int y = 100
        print("y =", y)
    catch:
        print("In second catch block")
    finally:
        print("In second finally block")
    fade
    
    print("After all try blocks")
}
'''
        output = self.capture_output(source)
        assert "=== First try block ===" in output
        assert "In first try block" in output
        assert "In first catch block - error caught!" in output
        assert "In first finally block" in output
        assert "=== Second try block ===" in output
        assert "In second try block" in output
        assert "y = 100" in output
        assert "In second finally block" in output
        assert "After all try blocks" in output
        # Second catch should not execute
        assert output.count("In second catch block") == 0

    def test_try_block_in_function(self):
        """Test try/catch/finally blocks inside functions."""
        source = '''
def str test_function() {
    try:
        print("In function try block")
        int x = 42
        x = "error"  # Type error
    catch:
        print("In function catch block - error caught!")
        # Note: return statements in blocks don't work yet (future enhancement)
    finally:
        print("In function finally block")
    fade
    
    return "Function completed"
}

def main() {
    var result = test_function()
    print("Function result:", result)
}
'''
        output = self.capture_output(source)
        assert "In function try block" in output
        assert "In function catch block - error caught!" in output
        assert "In function finally block" in output
        assert "Function result: Function completed" in output
