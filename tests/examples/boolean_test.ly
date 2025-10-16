def main() {
    print("Testing boolean and comparison operations...")
    
    # Test comparison operators
    a = 5
    b = 3
    c = 5
    
    print("a =", a, "b =", b, "c =", c)
    
    # Equality and inequality
    print("a == c:", a == c)
    print("a != b:", a != b)
    print("a == b:", a == b)
    
    # Ordering comparisons
    print("a > b:", a > b)
    print("a >= c:", a >= c)
    print("b < a:", b < a)
    print("b <= a:", b <= a)
    
    # Test with different types
    x = 10
    y = 10.0
    print("x == y (int vs float):", x == y)
    
    # Test logical operators
    print("---")
    print("Logical operators:")
    
    # AND operator
    print("true and true:", true and true)
    print("true and false:", true and false)
    print("false and true:", false and true)
    print("false and false:", false and false)
    
    # OR operator
    print("true or true:", true or true)
    print("true or false:", true or false)
    print("false or true:", false or true)
    print("false or false:", false or false)
    
    # NOT operator
    print("not true:", not true)
    print("not false:", not false)
    
    # Test truthiness rules
    print("---")
    print("Truthiness rules:")
    print("not 0:", not 0)
    print("not 1:", not 1)
    print("not 42:", not 42)
    print("not 0.0:", not 0.0)
    print("not 3.14:", not 3.14)
    print("not empty string:", not "")
    print("not hello string:", not "hello")
    
    # Test 'in' operator with range
    print("---")
    print("'in' operator:")
    print("3 in range(5):", 3 in range(5))
    print("7 in range(5):", 7 in range(5))
    print("0 in range(1, 5):", 0 in range(1, 5))
    print("3 in range(1, 5):", 3 in range(1, 5))
    
    # Complex boolean expressions
    print("---")
    print("Complex expressions:")
    age = 25
    has_license = true
    print("Can drive (age >= 18 and has_license):", age >= 18 and has_license)
    
    score = 85
    print("Grade A (score >= 90):", score >= 90)
    print("Grade B (score >= 80 and score < 90):", score >= 80 and score < 90)
}
