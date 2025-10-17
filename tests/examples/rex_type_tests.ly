# Test rex type and regex literal parsing - SPRINT5 Task 1
# Tests basic rex type functionality

def main() {
    print("=== Testing rex type and regex literals ===")
    
    # Test 1: Basic rex type declaration with regex literal
    rex pattern1 = /^abc/
    print("Test 1 - Basic rex declaration:")
    print("  Pattern:", pattern1)
    print("  Type:", type(pattern1))
    
    # Test 2: Complex regex pattern
    rex pattern2 = /[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}/
    print("\nTest 2 - Complex regex pattern:")
    print("  Pattern:", pattern2)
    print("  Type:", type(pattern2))
    
    # Test 3: Regex with escaped characters
    rex pattern3 = /hello\s+world/
    print("\nTest 3 - Regex with escaped characters:")
    print("  Pattern:", pattern3)
    print("  Type:", type(pattern3))
    
    # Test 4: Simple pattern
    rex pattern4 = /cat/
    print("\nTest 4 - Simple pattern:")
    print("  Pattern:", pattern4)
    print("  Type:", type(pattern4))
    
    # Test 5: Empty regex (valid)
    rex pattern5 = //
    print("\nTest 5 - Empty regex:")
    print("  Pattern:", pattern5)
    print("  Type:", type(pattern5))
    
    print("\n=== All rex type tests completed ===")
}
