# Performance Optimization Demo - Sprint 3 Task 5

def test_constant_folding() {
    print("=== Constant Folding Tests ===")
    
    # These expressions should be optimized at compile time
    result1 = 5 + 3 * 2
    result2 = (10 + 5) / 3
    result3 = 7 == 7
    result4 = !false
    result5 = -10
    
    print("result1 (5 + 3 * 2) =", result1)
    print("result2 ((10 + 5) / 3) =", result2)
    print("result3 (7 == 7) =", result3)
    print("result4 (!false) =", result4)
    print("result5 (-10) =", result5)
}

def test_variable_operations(x, y) {
    print("=== Variable Operations ===")
    
    # These involve variables, so they run at runtime
    sum = x + y
    product = x * y
    difference = x - y
    quotient = x / y
    
    print("x =", x, "y =", y)
    print("sum =", sum)
    print("product =", product)
    print("difference =", difference)
    print("quotient =", quotient)
    
    return sum + product + difference + quotient
}

def test_repeated_operations(base) {
    print("=== Repeated Operations (testing caching) ===")
    
    # Repeated access to the same variable
    result1 = base * 2
    result2 = base + base
    result3 = base - base
    result4 = base / 1
    
    print("base =", base)
    print("base * 2 =", result1)
    print("base + base =", result2)
    print("base - base =", result3)
    print("base / 1 =", result4)
    
    return result1 + result2 + result3 + result4
}

def main() {
    print("=== Performance Optimization Demo ===")
    print("This program demonstrates constant folding and caching optimizations.")
    print()
    
    # Test constant folding
    test_constant_folding()
    print()
    
    # Test variable operations
    result = test_variable_operations(15, 5)
    print("Total result from variable operations:", result)
    print()
    
    # Test repeated operations
    total = test_repeated_operations(10)
    print("Total from repeated operations:", total)
    print()
    
    print("=== Demo Complete ===")
}
