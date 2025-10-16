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
+++

def main() {
    print("=== Testing Counter Class ===")
    counter1 = Counter()
    counter2 = Counter()
    
    print("Initial count:", counter1.get_count())
    counter1.increment()
    counter1.increment()
    print("After 2 increments:", counter1.get_count())
    
    print("Second counter count:", counter2.get_count())
    counter2.increment()
    print("Second counter after increment:", counter2.get_count())
    
    print("First counter still:", counter1.get_count())
    
    print("\n=== Testing Person Class ===")
    person1 = Person()
    person1.set_info("Alice", 25)
    person1.greet()
    
    person2 = Person()
    person2.set_info("Bob", 30)
    person2.greet()
    
    print("Person1 still:", person1.name, person1.age)
}
