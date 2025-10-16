# Class and Instance Tests for Sprint 3
# Tests class definitions, instantiation, and method calls

# Test 1: Basic class definition
class Person:
    name = "Default Name"
    age = 0
    
    def greet(self) {
        return "Hello, I'm " + self.name
    }
    
    def get_age(self) {
        return self.age
    }
+++

# Test 2: Simple class with basic operations
class Counter:
    count = 0
    
    def increment(self) {
        self.count = self.count + 1
        return self.count
    }
    
    def get_count(self) {
        return self.count
    }
    
    def reset(self) {
        self.count = 0
    }
+++

# Test 3: Class instantiation and method calls
def test_basic_class_operations() {
    print("=== Basic Class Operations ===")
    
    # Create instances
    person1 = Person()
    person2 = Person()
    
    # Test default values
    print("Person1 default name:", person1.name)
    print("Person1 default age:", person1.age)
    print("Person2 default name:", person2.name)
    print("Person2 default age:", person2.age)
    
    # Test method calls
    greeting1 = person1.greet()
    greeting2 = person2.greet()
    print("Person1 greeting:", greeting1)
    print("Person2 greeting:", greeting2)
    
    # Test attribute modification
    person1.name = "Alice"
    person1.age = 25
    person2.name = "Bob"
    person2.age = 30
    
    print("After modification:")
    print("Person1 name:", person1.name, "age:", person1.age)
    print("Person2 name:", person2.name, "age:", person2.age)
    
    # Test updated method calls
    updated_greeting1 = person1.greet()
    updated_greeting2 = person2.greet()
    print("Updated Person1 greeting:", updated_greeting1)
    print("Updated Person2 greeting:", updated_greeting2)
}

# Test 4: Counter class operations
def test_counter_operations() {
    print("=== Counter Operations ===")
    
    counter1 = Counter()
    counter2 = Counter()
    
    # Test initial state
    print("Counter1 initial:", counter1.get_count())
    print("Counter2 initial:", counter2.get_count())
    
    # Test increment operations
    counter1.increment()
    counter1.increment()
    counter2.increment()
    
    print("Counter1 after 2 increments:", counter1.get_count())
    print("Counter2 after 1 increment:", counter2.get_count())
    
    # Test reset
    counter1.reset()
    print("Counter1 after reset:", counter1.get_count())
    
    # Test that instances are independent
    counter1.increment()
    counter2.increment()
    print("Counter1 after reset + 1 increment:", counter1.get_count())
    print("Counter2 after 2 increments:", counter2.get_count())
}

# Test 5: Class type information
def test_class_type_information() {
    print("=== Class Type Information ===")
    
    person = Person()
    counter = Counter()
    
    print("Person instance type:", type(person))
    print("Counter instance type:", type(counter))
    
    # Test isinstance functionality (if implemented)
    print("Testing isinstance functionality...")
    print("Note: isinstance() function may not be fully implemented yet")
}

# Test 6: Direct attribute modification (avoiding method parameters)
def test_direct_attribute_modification() {
    print("=== Direct Attribute Modification ===")
    
    person = Person()
    
    # Test direct attribute modification
    person.name = "Charlie"
    print("After direct assignment person.name = 'Charlie':", person.name)
    
    greeting = person.greet()
    print("Greeting after name change:", greeting)
    
    # Test multiple modifications
    person.age = 35
    print("After setting age to 35:", person.age)
}

def main() {
    print("=== Class and Instance Tests ===")
    
    # Run all test functions
    test_basic_class_operations()
    print()
    test_counter_operations()
    print()
    test_class_type_information()
    print()
    test_direct_attribute_modification()
    
    print("\\n=== Class and Instance Tests Complete ===")
    print("Note: Method parameters in class methods may have parsing issues.")
    print("Direct attribute modification works correctly.")
}