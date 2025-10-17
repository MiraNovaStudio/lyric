def main() {
    print("=== Try/Catch/Finally/Fade Syntax Demo ===")
    
    # Example 1: Try with catch and finally, no error
    print("\n1. Try block with no errors:")
    try:
        print("  Executing try block...")
        int x = 42
        str message = "Success!"
        print("  x =", x, "message =", message)
    catch:
        print("  Error caught (should not execute)")
    finally:
        print("  Cleanup in finally block")
    fade
    
    print("  After try/catch/finally block")
    
    # Example 2: Try with error, caught by catch
    print("\n2. Try block with error, caught by catch:")
    try:
        print("  Executing try block...")
        int y = 100
        y = "This will cause a type error"  # Type mismatch
    catch:
        print("  Error caught and handled!")
    finally:
        print("  Cleanup in finally block")
    fade
    
    print("  After try/catch/finally block")
    
    # Example 3: Try with only finally, error propagates
    print("\n3. Try block with only finally, error propagates:")
    try:
        print("  Executing try block...")
        int z = 200
        z = "This will cause a type error"  # Type mismatch
    finally:
        print("  Cleanup in finally block")
    fade
    
    print("  This line should not execute due to error propagation")
}

def demonstrate_nested_blocks() {
    print("\n=== Nested Try Blocks Demo ===")
    
    try:
        print("  In outer try block")
        try:
            print("    In inner try block")
            int x = 10
            x = "inner error"  # Type error in inner block
        catch:
            print("    Inner error caught!")
        finally:
            print("    Inner finally executed")
        fade
        print("  Back in outer try block")
    catch:
        print("  Outer error caught (should not execute)")
    finally:
        print("  Outer finally executed")
    fade
    
    print("  After nested try blocks")
}

def demonstrate_error_propagation() {
    print("\n=== Error Propagation Demo ===")
    
    # Error in catch block
    print("1. Error in catch block:")
    try:
        print("  In try block")
        int x = 42
        x = "first error"  # Type error
    catch:
        print("  In catch block")
        int y = 10
        y = "second error"  # Another type error
    finally:
        print("  Finally block executed")
    fade
    
    print("  This should not execute due to error in catch")
}

# Uncomment to run additional demos:
# demonstrate_nested_blocks()
# demonstrate_error_propagation()
