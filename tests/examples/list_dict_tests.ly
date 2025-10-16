# List and Dictionary Tests for Sprint 3
# Tests built-in data structures, indexing, and related operations

# Test 1: List creation and basic operations
numbers = [1, 2, 3, 4, 5]
fruits = ["apple", "banana", "orange"]
mixed = [1, "hello", true, 3.14]
empty_list = []

# Test 2: Dictionary creation and basic operations
person = {"name": "Alice", "age": 30, "city": "New York"}
scores = {"math": 95, "science": 87, "english": 92}
empty_dict = {}
nested_dict = {"user": {"name": "Bob", "preferences": {"theme": "dark"}}}

# Test 3: List indexing and operations
def test_list_operations() {
    print("=== List Operations ===")
    
    # Basic indexing
    print("numbers[0]:", numbers[0])
    print("numbers[2]:", numbers[2])
    print("fruits[1]:", fruits[1])
    
    # List length
    print("len(numbers):", len(numbers))
    print("len(fruits):", len(fruits))
    print("len(empty_list):", len(empty_list))
    
    # List modification (if supported)
    print("Original numbers:", numbers)
    # Note: append() would be tested if implemented
}

# Test 4: Dictionary operations
def test_dict_operations() {
    print("=== Dictionary Operations ===")
    
    # Basic key access
    print("person['name']:", person["name"])
    print("person['age']:", person["age"])
    print("scores['math']:", scores["math"])
    
    # Dictionary length
    print("len(person):", len(person))
    print("len(scores):", len(scores))
    print("len(empty_dict):", len(empty_dict))
    
    # Dictionary keys and values (if implemented)
    print("person keys:", keys(person))
    print("person values:", values(person))
}

# Test 5: Nested data structures
def test_nested_structures() {
    print("=== Nested Structures ===")
    
    # Nested list access
    print("mixed[0]:", mixed[0])
    print("mixed[1]:", mixed[1])
    print("mixed[2]:", mixed[2])
    print("mixed[3]:", mixed[3])
    
    # Nested dictionary access
    print("nested_dict['user']['name']:", nested_dict["user"]["name"])
    print("nested_dict['user']['preferences']['theme']:", nested_dict["user"]["preferences"]["theme"])
}

# Test 6: Data structure type information
def test_data_structure_types() {
    print("=== Data Structure Types ===")
    
    print("numbers type:", type(numbers))
    print("fruits type:", type(fruits))
    print("person type:", type(person))
    print("scores type:", type(scores))
    print("mixed type:", type(mixed))
    print("nested_dict type:", type(nested_dict))
}

# Test 7: Error handling for data structures
def test_data_structure_errors() {
    print("=== Data Structure Error Handling ===")
    
    # Test out of bounds access (should be handled gracefully)
    print("Testing out of bounds access...")
    # This might cause an error depending on implementation
    # invalid_index = numbers[10]
    print("Error handling test complete")
}

def main() {
    print("=== List and Dictionary Tests ===")
    
    # Run all test functions
    test_list_operations()
    print()
    test_dict_operations()
    print()
    test_nested_structures()
    print()
    test_data_structure_types()
    print()
    test_data_structure_errors()
    
    print("\\n=== List and Dictionary Tests Complete ===")
}
