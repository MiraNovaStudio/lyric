# Test nested scope resolution - SPRINT6 Task 1

def main() {
    print("=== Testing Nested Scope Resolution ===")
    
    # Test 1: Basic shadowing
    var x = "outer"
    print("\nTest 1 - Basic shadowing:")
    print("  Outer x:", x)
    
    if true:
        var x = "inner"
        print("  Inner x:", x)
    end
    
    print("  After block x:", x)
    
    # Test 2: Nested blocks
    var y = "level1"
    print("\nTest 2 - Nested blocks:")
    print("  Level 1 y:", y)
    
    if true:
        var y = "level2"
        print("  Level 2 y:", y)
        
        if true:
            var y = "level3"
            print("  Level 3 y:", y)
        end
        
        print("  Back to level 2 y:", y)
    end
    
    print("  Back to level 1 y:", y)
    
    # Test 3: Scope lookup order
    var a = "global"
    var b = "global_b"
    print("\nTest 3 - Scope lookup order:")
    
    if true:
        var a = "local"
        print("  a (local):", a)
        print("  b (global):", b)
    end
    
    # Test 4: Assignment to shadowed variable
    var z = "outer"
    print("\nTest 4 - Assignment to shadowed variable:")
    print("  Outer z:", z)
    
    if true:
        var z = "inner"
        z = "modified_inner"
        print("  Inner z (modified):", z)
    end
    
    print("  Outer z (unchanged):", z)
    
    # Test 5: Type preservation
    int num = 10
    print("\nTest 5 - Type preservation:")
    print("  Outer num:", num)
    
    if true:
        str num = "shadowed"
        print("  Inner num (str):", num)
    end
    
    print("  Outer num (int):", num)
    print("  Outer num type:", type(num))
    
    print("\n=== All nested scope tests completed ===")
}
