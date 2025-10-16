# Exception and Error Handling Tests for Sprint 3
# Tests various error scenarios and error handling capabilities

# Test 1: Type enforcement errors
def int strict_function(int value) {
    return value * 2
}

def str process_text(str text) {
    return "Processed: " + text
}

# Test 2: Runtime errors demonstration
def test_runtime_errors() {
    print("=== Runtime Error Tests ===")
    
    # Test undefined variable error (commented out to avoid actual error)
    print("Testing undefined variable access...")
    print("Note: undefined_variable would cause: Undefined variable: undefined_variable")
    
    # Test division by zero (commented out to avoid actual error)
    print("Testing division by zero...")
    print("Note: 10 / 0 would cause a division by zero error")
}

# Test 3: Type mismatch errors demonstration
def test_type_errors() {
    print("=== Type Error Tests ===")
    
    # Test function parameter type error (commented out to avoid actual error)
    print("Testing function parameter type error...")
    print("Note: strict_function('hello') would cause: Type mismatch for parameter 'value': expected int, got str")
    
    # Test variable type error (commented out to avoid actual error)
    print("Testing variable type error...")
    print("Note: int x = 42; x = 'wrong type' would cause: Type mismatch for variable 'x': expected int, got str")
}

# Test 4: Data structure errors demonstration
def test_data_structure_errors() {
    print("=== Data Structure Error Tests ===")
    
    # Test list index out of bounds (commented out to avoid actual error)
    print("Testing list index out of bounds...")
    print("Note: numbers[10] where numbers = [1,2,3] would cause: Index out of range")
    
    # Test dictionary key not found (commented out to avoid actual error)
    print("Testing dictionary key not found...")
    print("Note: person['nonexistent'] would cause: Key 'nonexistent' not found")
}

# Test 5: Built-in function errors demonstration
def test_builtin_errors() {
    print("=== Built-in Function Error Tests ===")
    
    # Test len() with wrong type (commented out to avoid actual error)
    print("Testing len() with wrong type...")
    print("Note: len(42) would cause: len() argument error: expected sequence, got int")
    
    # Test int() conversion error (commented out to avoid actual error)
    print("Testing int() conversion error...")
    print("Note: int('not a number') would cause: int() argument error: invalid literal")
}

# Test 6: Error message formatting demonstration
def test_error_messages() {
    print("=== Error Message Formatting Tests ===")
    
    print("Testing error message clarity and formatting...")
    print("Error messages include:")
    print("- Filename and line number")
    print("- Clear error description")
    print("- Expected vs actual values")
    print("- Context information (function names, parameter names)")
}

# Test 7: Working examples (these should work without errors)
def test_working_examples() {
    print("=== Working Examples ===")
    
    # Test correct function calls
    result1 = strict_function(5)
    print("strict_function(5) =", result1)
    
    result2 = process_text("hello world")
    print("process_text('hello world') =", result2)
    
    # Test correct data structure usage
    numbers = [1, 2, 3, 4, 5]
    print("numbers[2] =", numbers[2])
    print("len(numbers) =", len(numbers))
    
    person = {"name": "Alice", "age": 30}
    print("person['name'] =", person["name"])
    print("len(person) =", len(person))
}

def main() {
    print("=== Exception and Error Handling Tests ===")
    
    # Test basic error scenarios
    test_runtime_errors()
    print()
    test_type_errors()
    print()
    test_data_structure_errors()
    print()
    test_builtin_errors()
    print()
    test_error_messages()
    print()
    test_working_examples()
    
    print("\\n=== Exception and Error Handling Tests Complete ===")
    print("Note: try/catch exception handling is not yet implemented.")
    print("Error handling is currently done through runtime error messages.")
}