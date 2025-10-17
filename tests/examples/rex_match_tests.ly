# Test rex .match() method functionality - SPRINT5 Task 2
# Demonstrates comprehensive .match() usage

def main() {
    print("=== Testing rex .match() Method ===")
    
    # Test 1: Basic pattern matching
    rex pattern1 = /^abc/
    var result1 = pattern1.match("abcdef")
    var result2 = pattern1.match("xyz")
    print("Test 1 - Basic pattern matching:")
    print("  pattern.match('abcdef'):", result1)
    print("  pattern.match('xyz'):", result2)
    
    # Test 2: String variable matching
    rex pattern2 = /^[a-zA-Z]+$/
    var text1 = "hello"
    var text2 = "hello123"
    var result3 = pattern2.match(text1)
    var result4 = pattern2.match(text2)
    print("\nTest 2 - String variable matching:")
    print("  pattern.match('hello'):", result3)
    print("  pattern.match('hello123'):", result4)
    
    # Test 3: Complex email pattern
    rex email_pattern = /^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$/
    var email1 = "user@example.com"
    var email2 = "invalid-email"
    var email_result1 = email_pattern.match(email1)
    var email_result2 = email_pattern.match(email2)
    print("\nTest 3 - Email pattern matching:")
    print("  email_pattern.match('user@example.com'):", email_result1)
    print("  email_pattern.match('invalid-email'):", email_result2)
    
    # Test 4: Digit-only pattern
    rex digit_pattern = /^\d+$/
    var num1 = "123"
    var num2 = "abc"
    var num3 = "123abc"
    var digit_result1 = digit_pattern.match(num1)
    var digit_result2 = digit_pattern.match(num2)
    var digit_result3 = digit_pattern.match(num3)
    print("\nTest 4 - Digit pattern matching:")
    print("  digit_pattern.match('123'):", digit_result1)
    print("  digit_pattern.match('abc'):", digit_result2)
    print("  digit_pattern.match('123abc'):", digit_result3)
    
    # Test 5: Empty string pattern
    rex empty_pattern = /^$/
    var empty_string = ""
    var non_empty = "not empty"
    var empty_result1 = empty_pattern.match(empty_string)
    var empty_result2 = empty_pattern.match(non_empty)
    print("\nTest 5 - Empty string pattern:")
    print("  empty_pattern.match(''):", empty_result1)
    print("  empty_pattern.match('not empty'):", empty_result2)
    
    # Test 6: Boolean type verification
    rex test_pattern = /^test$/
    var bool_result = test_pattern.match("test")
    print("\nTest 6 - Boolean type verification:")
    print("  Result type:", type(bool_result))
    print("  Result value:", bool_result)
    
    if bool_result:
        print("  Boolean evaluation: True")
    else:
        print("  Boolean evaluation: False")
    end
    
    print("\n=== All .match() tests completed ===")
}
