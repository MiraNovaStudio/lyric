class Person:
name = "Unknown"
age = 0
def get_info() { return "Name: " + self.name + ", Age: " + str(self.age) }
+++

def main() {
    print("=== Testing isinstance function comprehensively ===")
    
    # Test all basic types
    print("Integer:", isinstance(42, "int"))
    print("Float:", isinstance(3.14, "float"))
    print("String:", isinstance("hello", "str"))
    print("Boolean:", isinstance(true, "bool"))
    print("None:", isinstance(None, "None"))
    
    # Test class instances
    person = Person()
    print("Person instance:", isinstance(person, "Person"))
    print("Person as int:", isinstance(person, "int"))
    print("Person as str:", isinstance(person, "str"))
    
    # Test edge cases
    print("String as int:", isinstance("42", "int"))
    print("Float as int:", isinstance(3.0, "int"))
    
    print("\n=== Testing type function comprehensively ===")
    
    # Test all basic types
    print("Integer type:", type(42))
    print("Float type:", type(3.14))
    print("String type:", type("hello"))
    print("Boolean type:", type(true))
    print("None type:", type(None))
    
    # Test class instances
    print("Person type:", type(person))
    
    # Test edge cases
    print("String '42' type:", type("42"))
    print("Float 3.0 type:", type(3.0))
    
    print("\n=== Testing range(start, stop) function ===")
    
    # Test various ranges
    print("range(0, 5):", range(0, 5))
    print("range(1, 4):", range(1, 4))
    print("range(-3, 3):", range(-3, 3))
    print("range(10, 15):", range(10, 15))
    print("range(0, 0):", range(0, 0))
    print("range(1, 1):", range(1, 1))
    
    # Test with variables
    start = 2
    stop = 7
    print("range(start, stop):", range(start, stop))
    
    print("\n=== Testing improved print function ===")
    
    # Test None handling
    print("Just None:", None)
    print("None with text:", "Value is", None)
    print("Multiple None:", None, None, None)
    
    # Test mixed types with None
    print("Mixed:", 42, None, "hello", None, true)
    
    # Test complex expressions
    print("Expression result:", isinstance(person, "Person"), type(person), None)
}
