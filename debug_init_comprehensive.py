from lyric.parser import parse
from lyric.interpreter import evaluate

# Test 1: Class with init() method
source1 = '''
class Person:
    def init(name, age) {
        self.name = name
        self.age = age
    }
    def greet() {
        print("Hello, I'm", self.name, "and I'm", self.age, "years old")
    }
+++

def main() {
    person = Person("Alice", 30)
    person.greet()
}'''

# Test 2: Class without init() method (should still work)
source2 = '''
class Point:
    x = 0
    y = 0
    def move(dx, dy) {
        self.x = self.x + dx
        self.y = self.y + dy
    }
+++

def main() {
    point = Point()
    point.move(5, 10)
    print("Point:", point.x, point.y)
}'''

print("=== Test 1: Class with init() ===")
try:
    ast1 = parse(source1)
    result1 = evaluate(ast1)
    print("Success:", result1)
except Exception as e:
    print("Error:", e)

print("\n=== Test 2: Class without init() ===")
try:
    ast2 = parse(source2)
    result2 = evaluate(ast2)
    print("Success:", result2)
except Exception as e:
    print("Error:", e)
