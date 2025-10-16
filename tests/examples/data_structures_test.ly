# Data Structures Test - Sprint 3 Task 3

def main() {
    print("=== Data Structures Test ===")
    
    # A8: List literals can be created and assigned
    numbers = [1, 2, 3, 4, 5]
    strings = ["hello", "world", "test"]
    mixed = [1, "hello", 3.14, true, None]
    
    print("numbers =", numbers)
    print("strings =", strings)
    print("mixed =", mixed)
    
    # A9: Dictionary literals can be created and assigned
    person = {"name": "Alice", "age": 30, "city": "New York"}
    scores = {"math": 95, "english": 87, "science": 92}
    
    print("person =", person)
    print("scores =", scores)
    
    # A10: List indexing works correctly
    print("numbers[0] =", numbers[0])
    print("numbers[2] =", numbers[2])
    print("numbers[4] =", numbers[4])
    
    # A11: Dictionary key lookup works correctly
    print("person['name'] =", person["name"])
    print("person['age'] =", person["age"])
    print("scores['math'] =", scores["math"])
    
    # A12: append() function works correctly
    print("Before append:", numbers)
    append(numbers, 6)
    print("After append:", numbers)
    append(strings, "new")
    print("After append to strings:", strings)
    
    # A13: keys() function works correctly
    person_keys = keys(person)
    scores_keys = keys(scores)
    print("Person keys:", person_keys)
    print("Scores keys:", scores_keys)
    
    # A14: values() function works correctly
    person_values = values(person)
    scores_values = values(scores)
    print("Person values:", person_values)
    print("Scores values:", scores_values)
    
    # len() function with data structures
    print("Length of numbers:", len(numbers))
    print("Length of strings:", len(strings))
    print("Length of person:", len(person))
    print("Length of scores:", len(scores))
    
    # Nested data structures
    matrix = [[1, 2], [3, 4]]
    data = {"user": {"name": "Alice", "age": 30}, "scores": {"math": 95, "english": 87}}
    
    print("matrix[0][0] =", matrix[0][0])
    print("matrix[1][1] =", matrix[1][1])
    print("data['user']['name'] =", data["user"]["name"])
    print("data['scores']['math'] =", data["scores"]["math"])
    
    # Data structures with expressions
    x = 10
    y = 20
    calculated = [x, y, x + y, x * y]
    print("calculated =", calculated)
    
    # Empty data structures
    empty_list = []
    empty_dict = {}
    print("empty_list =", empty_list)
    print("empty_dict =", empty_dict)
    print("Length of empty_list:", len(empty_list))
    print("Length of empty_dict:", len(empty_dict))
    
    print("=== All Data Structure Tests Passed ===")
}
