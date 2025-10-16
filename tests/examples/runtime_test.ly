class TestClass:
value = 42
def get_value() { return self.value }
+++

def main() {
    print("=== Testing isinstance function ===")
    
    # Test basic types
    print("isinstance(42, 'int'):", isinstance(42, "int"))
    print("isinstance(3.14, 'float'):", isinstance(3.14, "float"))
    print("isinstance('hello', 'str'):", isinstance("hello", "str"))
    print("isinstance(true, 'bool'):", isinstance(true, "bool"))
    print("isinstance(None, 'None'):", isinstance(None, "None"))
    
    # Test class instances
    obj = TestClass()
    print("isinstance(obj, 'TestClass'):", isinstance(obj, "TestClass"))
    print("isinstance(obj, 'int'):", isinstance(obj, "int"))
    
    print("\n=== Testing type function ===")
    
    # Test basic types
    print("type(42):", type(42))
    print("type(3.14):", type(3.14))
    print("type('hello'):", type("hello"))
    print("type(true):", type(true))
    print("type(None):", type(None))
    
    # Test class instances
    print("type(obj):", type(obj))
    
    print("\n=== Testing range function ===")
    
    # Test range(start, stop)
    print("range(2, 5):", range(2, 5))
    print("range(0, 3):", range(0, 3))
    print("range(-2, 2):", range(-2, 2))
    
    print("\n=== Testing improved print function ===")
    
    # Test None handling
    print("None value:", None)
    print("Mixed with None:", "hello", None, "world")
    
    # Test list handling (if lists are supported)
    # Note: Lists aren't directly supported in Lyric yet, but the print function is ready
}
