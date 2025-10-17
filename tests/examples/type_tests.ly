# Type System Tests for Sprint 3
# Tests type declarations, inference, and enforcement

# Test 1: Basic type declarations
int age = 25
float pi = 3.14159
str name = "Aeonath"
god is_active = true
None null_value = None

# Test 2: Type inference
var auto_int = 42
var auto_float = 2.718
var auto_string = "inferred"
var auto_god = false
var auto_none = None

# Test 3: Function with type declarations
def int add_numbers(int a, int b) {
    return a + b
}

def str format_greeting(str name, int age) {
    return "Hello " + name + ", you are " + str(age) + " years old"
}

def god is_even(int number) {
    if number % 2 == 0:
        return true
    else:
        return false
    end
}

def None do_nothing() {
    print("Doing nothing...")
}

# Test 4: Type enforcement (should cause errors when called with wrong types)
def int strict_add(int x, int y) {
    return x + y
}

def str process_name(str input_name) {
    return "Processed: " + input_name
}

def main() {
    print("=== Type System Tests ===")
    
    # Test basic type declarations
    print("1. Basic type declarations:")
    print("age:", age, "type:", type(age))
    print("pi:", pi, "type:", type(pi))
    print("name:", name, "type:", type(name))
    print("is_active:", is_active, "type:", type(is_active))
    print("null_value:", null_value, "type:", type(null_value))
    
    # Test type inference
    print("\n2. Type inference:")
    print("auto_int:", auto_int, "type:", type(auto_int))
    print("auto_float:", auto_float, "type:", type(auto_float))
    print("auto_string:", auto_string, "type:", type(auto_string))
    print("auto_god:", auto_god, "type:", type(auto_god))
    print("auto_none:", auto_none, "type:", type(auto_none))
    
    # Test function calls with correct types
    print("\n3. Function calls with correct types:")
    var result1 = add_numbers(10, 20)
    print("add_numbers(10, 20) =", result1)
    
    var greeting = format_greeting("Alice", 30)
    print("format_greeting result:", greeting)
    
    var even_check = is_even(16)
    print("is_even(16) =", even_check)
    
    do_nothing()
    
    # Test type enforcement with correct types
    print("\n4. Type enforcement tests (correct types):")
    var strict_result = strict_add(5, 3)
    print("strict_add(5, 3) =", strict_result)
    
    var processed = process_name("Bob")
    print("process_name result:", processed)
    
    print("\n=== Type System Tests Complete ===")
}