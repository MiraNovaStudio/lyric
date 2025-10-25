class Calculator:
    var name
    var history
    
    def Calculator(str name) {
        self.name = name
        self.history = []
        print("Calculator created:", self.name)
    }
    
    def add(int a, int b) {
        var result = a + b
        append(self.history, str(a) + " + " + str(b) + " = " + str(result))
        return result
    }
+++

def main() {
    calc = Calculator("MyCalc")
    result = calc.add(5, 3)
    print("Result:", result)
    print("History:", calc.history)
}
