# Comprehensive integration test for all Sprint 2 features

class Counter:
count = 0
def increment() { self.count = self.count + 1 }
def get_count() { return self.count }
def reset() { self.count = 0 }
+++

class Person:
name = "Unknown"
age = 0
def set_info(n, a) { 
    self.name = n
    self.age = a 
}
def greet() { print("Hello, I'm", self.name, "and I'm", self.age, "years old") }
def is_adult() { return self.age >= 18 }
+++

def main() {
    print("=== SPRINT 2 INTEGRATION TEST ===")
    
    print("\n1. Testing Nested Control Flow...")
    # Test nested if statements
    x = 5
    if x > 3:
        print("x > 3: true")
        if x > 4:
            print("x > 4: true")
            if x == 5:
                print("x == 5: true")
            end
        end
    end
    
    # Test nested loops
    print("Nested loops:")
    given i in range(2):
        given j in range(3):
            print("i:", i, "j:", j)
        done
    done
    
    print("\n2. Testing Boolean and Comparison Operations...")
    a = 10
    b = 5
    
    print("a =", a, "b =", b)
    print("a == b:", a == b)
    print("a != b:", a != b)
    print("a > b:", a > b)
    print("a < b:", a < b)
    print("a >= b:", a >= b)
    print("a <= b:", a <= b)
    
    print("true and false:", true and false)
    print("true or false:", true or false)
    print("not true:", not true)
    print("not false:", not false)
    
    print("5 in range(10):", 5 in range(10))
    print("15 in range(10):", 15 in range(10))
    
    print("\n3. Testing Class Instantiation and Methods...")
    # Test Counter class
    counter1 = Counter()
    counter2 = Counter()
    
    print("Counter instances created")
    print("counter1 count:", counter1.get_count())
    print("counter2 count:", counter2.get_count())
    
    counter1.increment()
    counter1.increment()
    counter2.increment()
    
    print("After increments:")
    print("counter1 count:", counter1.get_count())
    print("counter2 count:", counter2.get_count())
    
    # Test Person class
    person1 = Person()
    person1.set_info("Alice", 25)
    person1.greet()
    
    person2 = Person()
    person2.set_info("Bob", 16)
    person2.greet()
    
    print("Alice is adult:", person1.is_adult())
    print("Bob is adult:", person2.is_adult())
    
    print("\n4. Testing Runtime Enhancements...")
    # Test isinstance
    print("isinstance(42, 'int'):", isinstance(42, "int"))
    print("isinstance(person1, 'Person'):", isinstance(person1, "Person"))
    print("isinstance(person1, 'Counter'):", isinstance(person1, "Counter"))
    
    # Test type
    print("type(42):", type(42))
    print("type(person1):", type(person1))
    print("type(None):", type(None))
    
    # Test range
    print("range(2, 6):", range(2, 6))
    
    # Test enhanced print
    print("Print with None:", "Value is", None)
    
    print("\n5. Testing Comments...")
    # This is a comment
    print("Comments work!") # inline comment
    
    print("\n=== ALL SPRINT 2 FEATURES WORKING ===")
}
