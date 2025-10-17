def main() {
    print("=== Raise Keyword and Error Hierarchy Demo ===")
    
    # Example 1: Simple string raise
    print("\n1. Simple string raise:")
    try:
        raise "This is a simple error message"
    catch:
        print("  Caught: Simple string error")
    fade
    
    # Example 2: Typed exceptions
    print("\n2. Typed exceptions:")
    try:
        raise TypeError("This is a type error")
    catch:
        print("  Caught: Type error")
    fade
    
    try:
        raise ValueError("This is a value error")
    catch:
        print("  Caught: Value error")
    fade
    
    try:
        raise NameError("This is a name error")
    catch:
        print("  Caught: Name error")
    fade
    
    try:
        raise RuntimeError("This is a runtime error")
    catch:
        print("  Caught: Runtime error")
    fade
    
    # Example 3: Raise with variable message
    print("\n3. Raise with variable message:")
    str error_msg = "Error from variable"
    try:
        raise ValueError(error_msg)
    catch:
        print("  Caught: Variable message error")
    fade
    
    # Example 4: Raise with expression message
    print("\n4. Raise with expression message:")
    int error_code = 404
    str resource = "file.txt"
    try:
        raise RuntimeError("Error " + str(error_code) + " accessing " + resource)
    catch:
        print("  Caught: Expression message error")
    fade
    
    # Example 5: Raise in function
    print("\n5. Raise in function:")
    try:
        var result = test_function()
        print("  Function returned:", result)
    catch:
        print("  Caught: Function error")
    fade
    
    # Example 6: Nested try/catch with raise
    print("\n6. Nested try/catch with raise:")
    try:
        print("  In outer try block")
        try:
            print("  In inner try block")
            raise ValueError("Inner error")
        catch:
            print("  Caught inner error")
            raise TypeError("Outer error")
        fade
    catch:
        print("  Caught outer error")
    fade
    
    # Example 7: Raise in conditional
    print("\n7. Raise in conditional:")
    int x = 5
    try:
        if x > 3:
            raise ValueError("Value too large")
        else:
            print("  Value is acceptable")
        end
    catch:
        print("  Caught: Conditional raise error")
    fade
    
    print("\n=== Raise Demo Complete ===")
}

def str test_function() {
    raise NameError("Function error")
    return "This should not execute"
}
