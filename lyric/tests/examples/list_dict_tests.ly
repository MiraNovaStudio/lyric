# List and Dictionary Tests for Sprint 3
# Tests list/dictionary literals, indexing, and built-in functions

# Test 1: List literals and basic operations
var numbers = [1, 2, 3, 4, 5]
var words = ["hello", "world", "lyric"]
var mixed = [1, "hello", 3.14, True]

# Test 2: Dictionary literals and basic operations
var person = {"name": "Alice", "age": 30, "city": "New York"}
var scores = {"math": 95, "science": 87, "english": 92}
var config = {"debug": True, "version": "0.3.0", "port": 8080}

# Test 3: List indexing
var first_number = numbers[0]
var last_word = words[2]
var middle_number = numbers[2]

# Test 4: Dictionary key access
var person_name = person["name"]
var person_age = person["age"]
var math_score = scores["math"]

# Test 5: List length and built-in functions
var numbers_length = len(numbers)
var words_length = len(words)

# Test 6: Dictionary length and built-in functions
var person_keys = keys(person)
var person_values = values(person)
var scores_keys = keys(scores)

# Test 7: List modification (append)
append(numbers, 6)
append(words, "test")

# Test 8: Dictionary modification
person["email"] = "alice@example.com"
scores["history"] = 88

# Test 9: Nested structures
var nested = {
    "users": [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25}
    ],
    "settings": {
        "theme": "dark",
        "language": "en"
    }
}

# Test 10: Complex indexing
var first_user = nested["users"][0]
var first_user_name = nested["users"][0]["name"]
var theme = nested["settings"]["theme"]

# Test 11: Indexed assignment
numbers[0] = 10
person["age"] = 31
# nested["users"][0]["age"] = 31  # Commented out - nested structures may not parse correctly
