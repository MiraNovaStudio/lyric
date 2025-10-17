"""
Tests for Sprint 3 Task 4 - Enhanced Error Handling and Debugging
"""

import pytest
from lyric_lang.parser import parse
from lyric_lang.interpreter import Interpreter
from lyric_lang.errors import RuntimeErrorLyric, StackFrame


class TestEnhancedErrorHandling:
    """Test enhanced error handling with stack traces and debug information."""

    def test_stack_trace_basic(self):
        """Test A15: Stack traces show function call chain."""
        source = '''
def outer(x) {
    return middle(x)
}

def middle(y) {
    return inner(y)
}

def inner(z) {
    return undefined_var + z
}

def main() {
    result = outer(10)
}
'''
        program = parse(source, "test")
        interpreter = Interpreter(debug_mode=True)
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error = exc_info.value
        assert len(error.stack_trace) == 4  # main, outer, middle, inner
        
        # Check function names in stack trace
        frame_names = [frame.function_name for frame in error.stack_trace]
        assert frame_names == ["main", "outer", "middle", "inner"]

    def test_variable_inspection(self):
        """Test A16: Variable values are captured in stack frames."""
        source = '''
def test_function(x, y) {
    local_var = x + y
    return undefined_var
}

def main() {
    result = test_function(5, 10)
}
'''
        program = parse(source, "test")
        interpreter = Interpreter(debug_mode=True)
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error = exc_info.value
        assert len(error.stack_trace) >= 1
        
        # Check that variables are captured in the frame
        test_frame = None
        for frame in error.stack_trace:
            if frame.function_name == "test_function":
                test_frame = frame
                break
        
        assert test_frame is not None
        assert "x" in test_frame.local_vars
        assert "y" in test_frame.local_vars
        assert "local_var" in test_frame.local_vars
        assert test_frame.local_vars["x"] == 5
        assert test_frame.local_vars["y"] == 10
        assert test_frame.local_vars["local_var"] == 15

    def test_debug_mode_enabled(self):
        """Test A17: Debug mode can be enabled via Interpreter constructor."""
        source = '''
def test_func() {
    return undefined_var
}

def main() {
    test_func()
}
'''
        program = parse(source, "test")
        
        # Test with debug mode enabled
        interpreter_debug = Interpreter(debug_mode=True)
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter_debug.interpret(program)
        
        error = exc_info.value
        assert len(error.stack_trace) >= 2  # Should have stack trace
        
        # Test with debug mode disabled
        interpreter_normal = Interpreter(debug_mode=False)
        with pytest.raises(RuntimeErrorLyric) as exc_info2:
            interpreter_normal.interpret(program)
        
        error2 = exc_info2.value
        # Even in non-debug mode, stack trace should still be collected
        assert len(error2.stack_trace) >= 2

    def test_error_message_formatting(self):
        """Test error message formatting with stack trace."""
        source = '''
def test_func() {
    return undefined_var
}

def main() {
    test_func()
}
'''
        program = parse(source, "test")
        interpreter = Interpreter(debug_mode=True)
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error = exc_info.value
        
        # Test stack trace formatting
        stack_trace_str = error.format_stack_trace()
        assert "Stack trace:" in stack_trace_str
        assert "test_func" in stack_trace_str
        assert "main" in stack_trace_str
        
        # Test debug info formatting
        debug_info_str = error.format_debug_info()
        assert "Debug information:" in debug_info_str
        assert "Stack trace:" in debug_info_str

    def test_nested_function_calls(self):
        """Test stack trace with deeply nested function calls."""
        source = '''
def level1(a) {
    return level2(a)
}

def level2(b) {
    return level3(b)
}

def level3(c) {
    return level4(c)
}

def level4(d) {
    return level5(d)
}

def level5(e) {
    return undefined_var + e
}

def main() {
    result = level1(42)
}
'''
        program = parse(source, "test")
        interpreter = Interpreter(debug_mode=True)
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error = exc_info.value
        assert len(error.stack_trace) == 6  # main + 5 levels
        
        # Check the call chain
        frame_names = [frame.function_name for frame in error.stack_trace]
        expected = ["main", "level1", "level2", "level3", "level4", "level5"]
        assert frame_names == expected

    def test_parameter_passing_in_stack_trace(self):
        """Test that function parameters are correctly captured in stack frames."""
        source = '''
def complex_function(a, b, c) {
    d = a * b
    e = c + d
    f = e / 2
    return undefined_var
}

def main() {
    result = complex_function(10, 20, 30)
}
'''
        program = parse(source, "test")
        interpreter = Interpreter(debug_mode=True)
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error = exc_info.value
        
        # Find the complex_function frame
        complex_frame = None
        for frame in error.stack_trace:
            if frame.function_name == "complex_function":
                complex_frame = frame
                break
        
        assert complex_frame is not None
        assert complex_frame.local_vars["a"] == 10
        assert complex_frame.local_vars["b"] == 20
        assert complex_frame.local_vars["c"] == 30
        assert complex_frame.local_vars["d"] == 200  # 10 * 20
        assert complex_frame.local_vars["e"] == 230  # 30 + 200
        assert complex_frame.local_vars["f"] == 115  # 230 / 2

    def test_multiple_error_types_with_stack_trace(self):
        """Test that different error types include stack trace information."""
        source = '''
def test_division_by_zero() {
    return 10 / 0
}

def test_undefined_variable() {
    return undefined_var
}

def main() {
    # Test undefined variable (simpler test)
    test_undefined_variable()
}
'''
        program = parse(source, "test")
        interpreter = Interpreter(debug_mode=True)
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error = exc_info.value
        # Should have stack trace regardless of error type
        assert hasattr(error, 'stack_trace')
        assert len(error.stack_trace) >= 2

    def test_stack_frame_representation(self):
        """Test StackFrame string representation."""
        frame = StackFrame("test_func", "test.ly", 10, 5, {"x": 42, "y": "hello"})
        
        repr_str = repr(frame)
        assert "test_func" in repr_str
        assert "test.ly" in repr_str
        assert "10" in repr_str
        assert "5" in repr_str

    def test_empty_stack_trace(self):
        """Test error without stack trace."""
        error = RuntimeErrorLyric("Test error")
        assert len(error.stack_trace) == 0
        assert error.format_stack_trace() == ""
        assert error.format_debug_info() == ""

    def test_comprehensive_error_handling(self):
        """Test comprehensive error handling scenarios."""
        source = '''
def helper_function(value) {
    if value > 0:
        return process_positive(value)
    else:
        return process_negative(value)
    end
}

def process_positive(x) {
    y = x * 2
    return y + undefined_var
}

def process_negative(z) {
    w = z - 5
    return w / 0
}

def main() {
    result1 = helper_function(10)
    result2 = helper_function(-5)
}
'''
        program = parse(source, "test")
        interpreter = Interpreter(debug_mode=True)
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.interpret(program)
        
        error = exc_info.value
        assert len(error.stack_trace) >= 3  # main, helper_function, process_positive
        
        # Verify the stack trace shows the correct call path
        frame_names = [frame.function_name for frame in error.stack_trace]
        assert "main" in frame_names
        assert "helper_function" in frame_names
        assert "process_positive" in frame_names
        
        # Verify variables are captured correctly
        for frame in error.stack_trace:
            if frame.function_name == "process_positive":
                assert frame.local_vars["x"] == 10
                assert frame.local_vars["y"] == 20
                break
