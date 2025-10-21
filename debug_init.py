from lyric.parser import parse
from lyric.interpreter import evaluate

source = '''
class Person:
    def init(name) {
        self.name = name
        self.age = 0
    }
    def greet() {
        print("Hello, I'm", self.name)
    }
+++

def main() {
    person = Person("Alice")
    person.greet()
}'''

try:
    ast = parse(source)
    result = evaluate(ast)
    print("Success:", result)
except Exception as e:
    print("Error:", e)
