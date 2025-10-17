# Test rex .replace() method functionality - SPRINT5 Task 3
# Demonstrates comprehensive .replace() usage

def main() {
    print("=== Testing rex .replace() Method ===")
    
    # Test 1: Basic replacement
    rex pattern1 = /cat/
    var result1 = pattern1.replace("the cat sat", "dog")
    print("Test 1 - Basic replacement:")
    print("  pattern.replace('the cat sat', 'dog'):", result1)
    
    # Test 2: Multiple matches
    var result2 = pattern1.replace("cat cat cat", "dog")
    print("  pattern.replace('cat cat cat', 'dog'):", result2)
    
    # Test 3: No matches
    var result3 = pattern1.replace("the dog sat", "cat")
    print("  pattern.replace('the dog sat', 'cat'):", result3)
    
    # Test 4: String variables
    rex pattern2 = /hello/
    var source_text = "hello world hello"
    var replacement = "hi"
    var result4 = pattern2.replace(source_text, replacement)
    print("\nTest 4 - String variables:")
    print("  Source:", source_text)
    print("  Replacement:", replacement)
    print("  Result:", result4)
    
    # Test 5: Complex patterns
    rex digit_pattern = /\d+/
    var result5 = digit_pattern.replace("I have 5 cats and 3 dogs", "many")
    print("\nTest 5 - Complex patterns:")
    print("  digit_pattern.replace('I have 5 cats and 3 dogs', 'many'):", result5)
    
    # Test 6: Word boundaries
    rex word_pattern = /\bcat\b/
    var result6 = word_pattern.replace("cat in the catalog", "dog")
    print("  word_pattern.replace('cat in the catalog', 'dog'):", result6)
    
    # Test 7: Whitespace normalization
    rex space_pattern = /\s+/
    var result7 = space_pattern.replace("hello    world    test", " ")
    print("  space_pattern.replace('hello    world    test', ' '):", result7)
    
    # Test 8: Email replacement
    rex email_pattern = /[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}/
    var result8 = email_pattern.replace("Contact user@example.com for help", "admin@company.com")
    print("  email_pattern.replace result:", result8)
    
    # Test 9: Case sensitivity
    rex case_pattern = /cat/
    var result9 = case_pattern.replace("Cat in the hat", "dog")
    var result10 = case_pattern.replace("CAT in the hat", "dog")
    print("\nTest 9 - Case sensitivity:")
    print("  case_pattern.replace('Cat in the hat', 'dog'):", result9)
    print("  case_pattern.replace('CAT in the hat', 'dog'):", result10)
    
    # Test 10: Empty strings
    rex empty_pattern = /test/
    var result11 = empty_pattern.replace("", "replacement")
    var result12 = empty_pattern.replace("test", "")
    print("\nTest 10 - Empty strings:")
    print("  empty_pattern.replace('', 'replacement'):", result11)
    print("  empty_pattern.replace('test', ''):", result12)
    
    # Test 11: Return type verification
    rex type_pattern = /cat/
    var result13 = type_pattern.replace("the cat sat", "dog")
    print("\nTest 11 - Return type verification:")
    print("  Result type:", type(result13))
    print("  Result value:", result13)
    
    # Test 12: Original string preservation
    var original = "the cat sat"
    var result14 = type_pattern.replace(original, "dog")
    print("\nTest 12 - Original string preservation:")
    print("  Original:", original)
    print("  Result:", result14)
    
    print("\n=== All .replace() tests completed ===")
}
