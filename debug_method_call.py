from lyric.parser import parse
from lyric.interpreter import evaluate

source = '''
class Test:
    def greet() {
        print("Hello")
    }
+++

def main() {
    test = Test()
    test.greet()
}'''

try:
    ast = parse(source)
    result = evaluate(ast)
    print("Success:", result)
except Exception as e:
    print("Error:", e)
