# Lyric Programming Language
# Copyright (c) 2025 MiraNova Studios
# Designed and Architected by Michael (Aeonath) and ChatGPT
# Implemented by Claude
# Licensed under the MIT License with Source Attribution

"""
Comprehensive test suite for range() built-in function edge cases.
Tests negative steps, zero step errors, negative values, and type validation.
"""

import pytest
from lyric.parser import parse
from lyric.interpreter import Interpreter, evaluate
from lyric.errors import RuntimeErrorLyric, TypeErrorLyric


class TestRangeNegativeStep:
    """Test range() with negative step values (countdown)."""
    
    def test_range_negative_step_countdown(self):
        """Test range countdown from 5 to 1."""
        code = """
var count = 0
given i in range(5, 0, -1):
    count = count + 1
done
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(5, 0, -1) should produce [5, 4, 3, 2, 1] = 5 iterations
        assert interpreter.global_scope['count'] == 5
    
    def test_range_negative_step_with_negatives(self):
        """Test range with negative start/stop and negative step."""
        code = """
var items = []
given i in range(-1, -6, -1):
    items = items + [i]
done
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        from lyric.interpreter import ArrObject
        items = interpreter.global_scope['items']
        assert isinstance(items, ArrObject)
        # range(-1, -6, -1) should produce [-1, -2, -3, -4, -5]
        assert items.elements == [-1, -2, -3, -4, -5]
    
    def test_range_negative_step_by_two(self):
        """Test range with negative step of -2."""
        code = """
var items = []
given i in range(10, 0, -2):
    items = items + [i]
done
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        from lyric.interpreter import ArrObject
        items = interpreter.global_scope['items']
        assert isinstance(items, ArrObject)
        # range(10, 0, -2) should produce [10, 8, 6, 4, 2]
        assert items.elements == [10, 8, 6, 4, 2]


class TestRangeZeroStep:
    """Test range() with zero step (should raise error)."""
    
    def test_range_zero_step_raises_error(self):
        """Test that range with step=0 raises a ValueError."""
        code = """
var items = []
given i in range(0, 5, 0):
    items = items + [i]
done
"""
        ast = parse(code)
        interpreter = Interpreter()
        
        # Python's range(0, 5, 0) raises ValueError: range() arg 3 must not be zero
        with pytest.raises((ValueError, RuntimeErrorLyric)):
            interpreter.evaluate(ast)


class TestRangeNegativeValues:
    """Test range() with negative start/stop values."""
    
    def test_range_negative_to_positive(self):
        """Test range from negative to positive."""
        code = """
var items = []
given i in range(-5, 5):
    items = items + [i]
done
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        from lyric.interpreter import ArrObject
        items = interpreter.global_scope['items']
        assert isinstance(items, ArrObject)
        # range(-5, 5) should produce [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4]
        assert items.elements == [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4]
    
    def test_range_negative_start(self):
        """Test range starting from negative number."""
        code = """
var items = []
given i in range(-3, 2):
    items = items + [i]
done
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        from lyric.interpreter import ArrObject
        items = interpreter.global_scope['items']
        assert isinstance(items, ArrObject)
        # range(-3, 2) should produce [-3, -2, -1, 0, 1]
        assert items.elements == [-3, -2, -1, 0, 1]
    
    def test_range_both_negative(self):
        """Test range with both negative start and stop."""
        code = """
var items = []
given i in range(-10, -5):
    items = items + [i]
done
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        from lyric.interpreter import ArrObject
        items = interpreter.global_scope['items']
        assert isinstance(items, ArrObject)
        # range(-10, -5) should produce [-10, -9, -8, -7, -6]
        assert items.elements == [-10, -9, -8, -7, -6]
    
    def test_range_negative_with_step(self):
        """Test range with negative start and positive step."""
        code = """
var items = []
given i in range(-10, 0, 2):
    items = items + [i]
done
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        from lyric.interpreter import ArrObject
        items = interpreter.global_scope['items']
        assert isinstance(items, ArrObject)
        # range(-10, 0, 2) should produce [-10, -8, -6, -4, -2]
        assert items.elements == [-10, -8, -6, -4, -2]


class TestRangeEmptyRanges:
    """Test range() that should produce empty sequences."""
    
    def test_range_empty_start_equals_stop(self):
        """Test range where start equals stop."""
        code = """
var count = 0
given i in range(5, 5):
    count = count + 1
done
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(5, 5) should be empty
        assert interpreter.global_scope['count'] == 0
    
    def test_range_empty_start_greater_than_stop_positive_step(self):
        """Test range where start > stop with positive step."""
        code = """
var count = 0
given i in range(10, 5, 1):
    count = count + 1
done
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(10, 5, 1) should be empty (can't count up from 10 to 5)
        assert interpreter.global_scope['count'] == 0
    
    def test_range_empty_start_less_than_stop_negative_step(self):
        """Test range where start < stop with negative step."""
        code = """
var count = 0
given i in range(5, 10, -1):
    count = count + 1
done
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(5, 10, -1) should be empty (can't count down from 5 to 10)
        assert interpreter.global_scope['count'] == 0
    
    def test_range_single_arg_zero(self):
        """Test range(0) produces empty sequence."""
        code = """
var count = 0
given i in range(0):
    count = count + 1
done
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(0) should be empty
        assert interpreter.global_scope['count'] == 0
    
    def test_range_single_arg_negative(self):
        """Test range with negative single argument produces empty sequence."""
        code = """
var count = 0
given i in range(-5):
    count = count + 1
done
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(-5) should be empty
        assert interpreter.global_scope['count'] == 0


class TestRangeTypeValidation:
    """Test range() type validation and error handling."""
    
    def test_range_with_float_argument(self):
        """Test that range rejects float arguments."""
        code = """
var items = []
given i in range(5.5):
    items = items + [i]
done
"""
        ast = parse(code)
        interpreter = Interpreter()
        
        # Python's range() requires integers
        with pytest.raises((TypeError, RuntimeErrorLyric)):
            interpreter.evaluate(ast)
    
    def test_range_with_string_argument(self):
        """Test that range rejects string arguments."""
        code = """
var items = []
given i in range("5"):
    items = items + [i]
done
"""
        ast = parse(code)
        interpreter = Interpreter()
        
        # Python's range() requires integers
        with pytest.raises((TypeError, RuntimeErrorLyric)):
            interpreter.evaluate(ast)
    
    def test_range_no_arguments_error(self):
        """Test that range with no arguments raises error."""
        code = """
var items = range()
"""
        ast = parse(code)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Invalid range() arguments" in error_msg or "takes 1-3 arguments" in error_msg
    
    def test_range_too_many_arguments_error(self):
        """Test that range with > 3 arguments raises error."""
        code = """
var items = range(1, 2, 3, 4)
"""
        ast = parse(code)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Invalid range() arguments" in error_msg
        assert "takes 1-3 arguments" in error_msg


class TestRangeLargeValues:
    """Test range() with large values."""
    
    def test_range_large_single_argument(self):
        """Test range with large single argument."""
        code = """
var items = range(10000)
var count = items.len()
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(10000) should produce 10000 items
        assert interpreter.global_scope['count'] == 10000
    
    def test_range_large_span(self):
        """Test range with large span."""
        code = """
var items = range(0, 5000, 10)
var count = items.len()
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(0, 5000, 10) should produce 500 items
        assert interpreter.global_scope['count'] == 500
    
    def test_range_large_negative_step(self):
        """Test range with large negative step."""
        code = """
var items = range(1000, 0, -10)
var count = items.len()
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(1000, 0, -10) should produce 100 items
        assert interpreter.global_scope['count'] == 100


class TestRangeInExpressions:
    """Test range() used in various expression contexts."""
    
    def test_range_direct_indexing(self):
        """Test indexing directly into range result."""
        code = """
var items = range(10, 20)
var first = items[0]
var last = items[9]
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(10, 20) produces [10, 11, ..., 19]
        assert interpreter.global_scope['first'] == 10
        assert interpreter.global_scope['last'] == 19
    
    def test_range_in_list_concatenation(self):
        """Test using range result in concatenation."""
        code = """
var prefix = [0, 1]
var combined = prefix + range(2, 5)
var length = combined.len()
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # [0, 1] + [2, 3, 4] = 5 items
        assert interpreter.global_scope['length'] == 5
    
    def test_range_with_arr_methods(self):
        """Test that range result supports arr methods."""
        code = """
var items = range(5, 10)
var max_val = items.max()
var min_val = items.min()
var total = items.sum()
"""
        ast = parse(code)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(5, 10) = [5, 6, 7, 8, 9]
        assert interpreter.global_scope['max_val'] == 9
        assert interpreter.global_scope['min_val'] == 5
        assert interpreter.global_scope['total'] == 35  # 5+6+7+8+9
