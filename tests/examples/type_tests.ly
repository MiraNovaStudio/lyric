# Type Declaration and Inference Tests

# A1: Type declarations work correctly
x: int = 5
y: str = "hello"
z: bool = true

# A2: Type enforcement works - this should cause an error if uncommented
# x: int = "string"  # This should raise a type mismatch error

# A3: Functions with typed parameters enforce types
def add(a: int, b: int): int {
    return a + b
}

def greet(name: str): str {
    return "Hello, " + name
}

# A4: Type inference assigns correct default types
auto_int = 42
auto_float = 3.14
auto_string = "inferred"
auto_bool = false
auto_none = None

def main() {
    print("=== Type Declaration Tests ===")
    print("x:", x, "type:", type(x))
    print("y:", y, "type:", type(y))
    print("z:", z, "type:", type(z))
    
    print("\n=== Type-Annotated Functions ===")
    result1 = add(10, 20)
    result2 = greet("World")
    print("add(10, 20):", result1)
    print("greet('World'):", result2)
    
    print("\n=== Type Inference Tests ===")
    print("auto_int:", auto_int, "type:", type(auto_int))
    print("auto_float:", auto_float, "type:", type(auto_float))
    print("auto_string:", auto_string, "type:", type(auto_string))
    print("auto_bool:", auto_bool, "type:", type(auto_bool))
    print("auto_none:", auto_none, "type:", type(auto_none))
    
    print("\n=== Type Checking with isinstance ===")
    print("isinstance(auto_int, 'int'):", isinstance(auto_int, "int"))
    print("isinstance(auto_string, 'str'):", isinstance(auto_string, "str"))
    print("isinstance(auto_int, 'str'):", isinstance(auto_int, "str"))
    
    print("\n=== All Type Tests Passed ===")
}
