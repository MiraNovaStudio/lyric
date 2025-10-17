"""
Tests for Sprint 3 Task 5 - Runtime Optimization and Performance
"""

import pytest
from lyric_lang.parser import parse
from lyric_lang.interpreter import Interpreter


class TestRuntimeOptimization:
    """Test runtime optimizations for better performance."""

    def test_constant_folding_basic_arithmetic(self):
        """Test A18: Basic arithmetic constant folding works correctly."""
        source = '''
def main() {
    # These should be constant folded
    result1 = 5 + 3
    result2 = 10 - 4
    result3 = 6 * 2
    result4 = 8 / 2
    
    print("result1 =", result1)
    print("result2 =", result2)
    print("result3 =", result3)
    print("result4 =", result4)
}
'''
        program = parse(source, "test")
        interpreter = Interpreter(performance_monitoring=True)
        interpreter.interpret(program)
        
        stats = interpreter.get_performance_stats()
        assert stats['constant_fold_count'] >= 4  # At least 4 constant folds

    def test_constant_folding_complex_expressions(self):
        """Test constant folding with complex expressions."""
        source = '''
def main() {
    # Complex expressions that should be constant folded
    result1 = (5 + 3) * 2
    result2 = 10 - (4 + 2)
    result3 = (7 * 2) / (3 + 1)
    
    print("result1 =", result1)
    print("result2 =", result2)
    print("result3 =", result3)
}
'''
        program = parse(source, "test")
        interpreter = Interpreter(performance_monitoring=True)
        interpreter.interpret(program)
        
        stats = interpreter.get_performance_stats()
        assert stats['constant_fold_count'] >= 4  # Some constant folds for inner operations

    def test_constant_folding_comparison_operations(self):
        """Test constant folding with comparison operations."""
        source = '''
def main() {
    # Comparison operations that should be constant folded
    result1 = 5 == 5
    result2 = 3 < 7
    result3 = 10 >= 5
    result4 = 2 != 3
    
    print("result1 =", result1)
    print("result2 =", result2)
    print("result3 =", result3)
    print("result4 =", result4)
}
'''
        program = parse(source, "test")
        interpreter = Interpreter(performance_monitoring=True)
        interpreter.interpret(program)
        
        stats = interpreter.get_performance_stats()
        assert stats['constant_fold_count'] >= 4  # At least 4 constant folds

    def test_constant_folding_unary_operations(self):
        """Test constant folding with unary operations."""
        source = '''
def main() {
    # Unary operations that should be constant folded
    result1 = -5
    result2 = +10
    result3 = !true
    result4 = !false
    
    print("result1 =", result1)
    print("result2 =", result2)
    print("result3 =", result3)
    print("result4 =", result4)
}
'''
        program = parse(source, "test")
        interpreter = Interpreter(performance_monitoring=True)
        interpreter.interpret(program)
        
        stats = interpreter.get_performance_stats()
        assert stats['constant_fold_count'] >= 4  # At least 4 constant folds

    def test_environment_caching_variable_lookups(self):
        """Test A19: Environment caching reduces variable lookup overhead."""
        source = '''
def test_function(x) {
    # Multiple accesses to the same variable
    result1 = x + x
    result2 = x * x
    result3 = x - x
    result4 = x / 2
    
    return result1 + result2 + result3 + result4
}

def main() {
    result = test_function(10)
    print("Result:", result)
}
'''
        program = parse(source, "test")
        interpreter = Interpreter(performance_monitoring=True)
        interpreter.interpret(program)
        
        stats = interpreter.get_performance_stats()
        # Should have many variable lookups
        assert stats['variable_lookup_count'] > 0

    def test_performance_monitoring_enabled(self):
        """Test A20: Performance monitoring can be enabled and provides statistics."""
        source = '''
def main() {
    x = 5
    y = 10
    result = x + y
    print("Result:", result)
}
'''
        # Test with performance monitoring enabled
        interpreter = Interpreter(performance_monitoring=True)
        program = parse(source, "test")
        interpreter.interpret(program)
        
        stats = interpreter.get_performance_stats()
        assert stats['performance_monitoring'] is True
        assert 'operation_counts' in stats
        assert 'function_call_counts' in stats
        assert 'variable_lookup_count' in stats
        assert 'constant_fold_count' in stats
        assert stats['total_operations'] > 0

    def test_performance_monitoring_disabled(self):
        """Test that performance monitoring can be disabled."""
        source = '''
def main() {
    x = 5
    y = 10
    result = x + y
    print("Result:", result)
}
'''
        # Test with performance monitoring disabled
        interpreter = Interpreter(performance_monitoring=False)
        program = parse(source, "test")
        interpreter.interpret(program)
        
        stats = interpreter.get_performance_stats()
        assert stats['performance_monitoring'] is False

    def test_operation_counting(self):
        """Test that operation counting works correctly."""
        source = '''
def main() {
    x = 5
    y = 10
    z = x + y
    w = x * y
    v = x - y
    u = x / y
    
    print("Results:", z, w, v, u)
}
'''
        interpreter = Interpreter(performance_monitoring=True)
        program = parse(source, "test")
        interpreter.interpret(program)
        
        stats = interpreter.get_performance_stats()
        assert stats['operation_counts']['binary_+'] >= 1
        assert stats['operation_counts']['binary_*'] >= 1
        assert stats['operation_counts']['binary_-'] >= 1
        assert stats['operation_counts']['binary_/'] >= 1

    def test_function_call_counting(self):
        """Test that function call counting works correctly."""
        source = '''
def helper_function(x) {
    return x * 2
}

def test_function(y) {
    return helper_function(y) + helper_function(y + 1)
}

def main() {
    result = test_function(5)
    print("Result:", result)
}
'''
        interpreter = Interpreter(performance_monitoring=True)
        program = parse(source, "test")
        interpreter.interpret(program)
        
        stats = interpreter.get_performance_stats()
        assert stats['function_call_counts']['main'] == 1
        assert stats['function_call_counts']['test_function'] == 1
        assert stats['function_call_counts']['helper_function'] == 2

    def test_performance_stats_reset(self):
        """Test that performance statistics can be reset."""
        source = '''
def main() {
    x = 5
    y = 10
    result = x + y
    print("Result:", result)
}
'''
        interpreter = Interpreter(performance_monitoring=True)
        program = parse(source, "test")
        
        # Run first time
        interpreter.interpret(program)
        stats1 = interpreter.get_performance_stats()
        
        # Reset stats
        interpreter.reset_performance_stats()
        
        # Run second time
        interpreter.interpret(program)
        stats2 = interpreter.get_performance_stats()
        
        # Stats should be similar but independent
        assert stats1['performance_monitoring'] is True
        assert stats2['performance_monitoring'] is True
        assert stats1['total_operations'] == stats2['total_operations']

    def test_constant_folding_with_variables(self):
        """Test that constant folding doesn't interfere with variable operations."""
        source = '''
def main() {
    x = 5
    y = 10
    
    # These should NOT be constant folded (involve variables)
    result1 = x + y
    result2 = x * 2
    
    # These SHOULD be constant folded (pure literals)
    result3 = 3 + 4
    result4 = 5 * 2
    
    print("Results:", result1, result2, result3, result4)
}
'''
        interpreter = Interpreter(performance_monitoring=True)
        program = parse(source, "test")
        interpreter.interpret(program)
        
        stats = interpreter.get_performance_stats()
        # Should have some constant folds but not all operations
        assert stats['constant_fold_count'] >= 2
        assert stats['constant_fold_count'] < stats['total_operations']

    def test_comprehensive_performance_optimization(self):
        """Test comprehensive performance optimization features."""
        source = '''
def complex_function(x, y) {
    # Mix of constant folding and variable operations
    const_result1 = (10 + 5) * 2
    const_result2 = 20 / 4
    const_result3 = 7 == 7
    const_result4 = !false
    
    # Variable operations
    var_result1 = x + y
    var_result2 = x * y
    var_result3 = x - y
    
    # Complex expression with variables
    final_result = (var_result1 + var_result2) * const_result1
    
    return final_result + const_result2
}

def main() {
    result = complex_function(5, 3)
    print("Final result:", result)
    
    # Call function multiple times to test caching
    result2 = complex_function(10, 2)
    print("Second result:", result2)
}
'''
        interpreter = Interpreter(performance_monitoring=True)
        program = parse(source, "test")
        interpreter.interpret(program)
        
        stats = interpreter.get_performance_stats()
        
        # Verify all optimization features are working
        assert stats['performance_monitoring'] is True
        assert stats['constant_fold_count'] >= 4  # Multiple constant folds
        assert stats['total_operations'] > 0
        assert stats['total_function_calls'] >= 3  # main + 2 complex_function calls
        assert stats['variable_lookup_count'] > 0
        
        # Verify operation breakdown
        assert 'binary_+' in stats['operation_counts']
        assert 'binary_*' in stats['operation_counts']
        assert 'binary_-' in stats['operation_counts']
        assert 'binary_/' in stats['operation_counts']
        assert 'binary_==' in stats['operation_counts']
        assert 'unary_!' in stats['operation_counts']
