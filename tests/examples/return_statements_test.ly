# Return Statements and Function Values Test

# A5: Functions can return values and assign them to variables
def get_number() {
    return 42
}

def add(a, b) {
    return a + b
}

def get_greeting() {
    return "Hello, World!"
}

def get_nothing() {
    # No return statement - defaults to None
}

# A6: print(add(2,3)) outputs the correct numeric result
def test_print_function_calls() {
    print("add(2, 3) =", add(2, 3))
    print("get_number() =", get_number())
    print("get_greeting() =", get_greeting())
}

# A7: Missing return defaults to None
def test_missing_return() {
    result = get_nothing()
    print("get_nothing() =", result)
    print("is None?", result == None)
}

def main() {
    print("=== Return Statements and Function Values Test ===")
    
    # A5: Return values assigned to variables
    x = get_number()
    y = add(10, 20)
    z = get_greeting()
    
    print("\nA5 - Return values assigned to variables:")
    print("x = get_number() =", x)
    print("y = add(10, 20) =", y)
    print("z = get_greeting() =", z)
    
    # A6: Direct function calls in print
    print("\nA6 - Direct function calls in print:")
    test_print_function_calls()
    
    # A7: Missing return defaults to None
    print("\nA7 - Missing return defaults to None:")
    test_missing_return()
    
    # Additional tests - Function values in expressions
    print("\nAdditional tests - Function values in expressions:")
    result1 = add(get_number(), get_number())
    result2 = add(1, add(2, 3))
    result3 = get_greeting() + " How are you?"
    
    print("add(get_number(), get_number()) =", result1)
    print("add(1, add(2, 3)) =", result2)
    print("get_greeting() + ' How are you?' =", result3)
    
    # Nested function calls
    print("\nNested function calls:")
    nested_result = add(add(1, 2), add(3, 4))
    print("add(add(1, 2), add(3, 4)) =", nested_result)
    
    print("\n=== All Return Statement Tests Passed ===")
}
