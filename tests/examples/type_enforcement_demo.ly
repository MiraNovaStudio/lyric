def main() {
    print("=== Type Enforcement Verification Demo ===")

    # Test 1 - Successful type assignments
    print("\n1. Successful Type Assignments:")
    int number = 42
    str text = "hello"
    god flag = true
    float pi = 3.14159
    rex pattern = /^test/
    list items = [1, 2, 3]
    dict person = {"name": "Alice", "age": 30}
    None value = None

    print("  number:", number, "type:", type(number))
    print("  text:", text, "type:", type(text))
    print("  flag:", flag, "type:", type(flag))
    print("  pi:", pi, "type:", type(pi))
    print("  pattern:", pattern, "type:", type(pattern))
    print("  items:", items, "type:", type(items))
    print("  person:", person, "type:", type(person))
    print("  value:", value, "type:", type(value))

    # Test 2 - Successful reassignments with same types
    print("\n2. Successful Reassignments:")
    number = 100
    text = "world"
    flag = false
    pi = 2.718
    pattern = /end$/
    items = ["a", "b", "c"]
    person = {"x": 1, "y": 2}

    print("  number after reassignment:", number)
    print("  text after reassignment:", text)
    print("  flag after reassignment:", flag)
    print("  pi after reassignment:", pi)
    print("  pattern after reassignment:", pattern)
    print("  items after reassignment:", items)
    print("  person after reassignment:", person)

    # Test 3 - Var type flexibility
    print("\n3. Var Type Flexibility:")
    var flexible = 42
    print("  flexible as int:", flexible, "type:", type(flexible))
    
    flexible = "now a string"
    print("  flexible as str:", flexible, "type:", type(flexible))
    
    flexible = true
    print("  flexible as god:", flexible, "type:", type(flexible))

    # Test 4 - Function with return type enforcement
    print("\n4. Function Return Type Enforcement:")
    
    def int get_number() {
        return 42
    }
    
    def str get_message() {
        return "hello from function"
    }
    
    var result1 = get_number()
    var result2 = get_message()
    print("  Function return 1:", result1, "type:", type(result1))
    print("  Function return 2:", result2, "type:", type(result2))

    # Test 5 - Function with parameter type enforcement
    print("\n5. Function Parameter Type Enforcement:")
    
    def str combine(int num, str text) {
        return str(num) + ": " + text
    }
    
    var combined = combine(123, "test")
    print("  Combined result:", combined)

    # Test 6 - Nested scope type enforcement
    print("\n6. Nested Scope Type Enforcement:")
    int outer_var = 10
    print("  Outer variable:", outer_var, "type:", type(outer_var))
    
    if true:
        str outer_var = "shadowed"
        print("  Inner variable (shadowed):", outer_var, "type:", type(outer_var))
    end
    
    print("  Outer variable after block:", outer_var, "type:", type(outer_var))

    print("\n=== Type Enforcement Demo Completed ===")
    print("Note: Type enforcement errors would raise RuntimeErrorLyric")
    print("with clear messages showing variable name, expected type, and actual type.")
}


