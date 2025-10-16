# Enhanced Error Handling Demo - Sprint 3 Task 4

def level1_function(x) {
    local_var = x * 2
    return level2_function(local_var)
}

def level2_function(y) {
    result = y + 10
    return level3_function(result)
}

def level3_function(z) {
    final_result = z / 2
    return final_result + undefined_variable
}

def main() {
    print("=== Enhanced Error Handling Demo ===")
    print("This program will demonstrate stack traces and variable inspection.")
    print()
    
    print("Calling level1_function(5)...")
    value = level1_function(5)
    print("Result:", value)
    
    print("=== Demo Complete ===")
}
