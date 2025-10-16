# This file demonstrates runtime errors (execution errors)

def main() {
    print("Testing various runtime errors...")
    
    # Error 1: Undefined variable
    print("Error 1 - Undefined variable:")
    print(undefined_variable)
    
    # Error 2: Calling undefined function
    print("Error 2 - Undefined function:")
    undefined_function()
    
    # Error 3: Wrong argument count
    print("Error 3 - Wrong argument count:")
    isinstance(42)  # Missing second argument
}
