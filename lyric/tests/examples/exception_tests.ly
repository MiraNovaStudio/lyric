
    var result1 = 10 / 0

var cleanup_done = False
    var result2 = 10 / 2

var x = 10
    var y = x / 0

def risky_function(int divisor) {
    if divisor == 0:
        raise ZeroDivisionErrorLyric
    end
    return 10 / divisor
}
def safe_divide(int a, int b) {
    try:
        return a / b
    catch:
        print("Division failed, returning 0")
        return 0
    finally:
        print("Division attempt completed")
    fade
}
var counter = 0
    var result3 = 10 / 0

class Calculator
    def divide(int a, int b) {
        try:
            return a / b
        catch:
            print("Division error in calculator")
            return 0
        fade
    }
+++

var calc = Calculator()
var result4 = calc.divide(10, 0)

    var append_result = append("not_a_list", 5)

    var numbers = [1, 2, 3]
    var index_result = numbers[10]

def main() {
    # Exception Handling Tests for Sprint 3
    # Tests try/catch/finally blocks and raise statements
    # Test 1: Basic try/catch
    try:
    catch:
        print("Caught division by zero error")
    fade
    # Test 2: Try/catch with finally
    try:
        print("Division successful:", result2)
    catch:
        print("Caught an error")
    finally:
        cleanup_done = True
        print("Cleanup completed")
    fade
    # Test 3: Try/catch with variable access
    try:
    catch:
        x = 20  # Modify variable in catch block
    finally:
        print("Final x value:", x)
    fade
    # Test 4: Raise different exception types
    # raise RuntimeErrorLyric
    # raise IndexErrorLyric
    # raise TypeErrorLyric
    # raise ValueErrorLyric
    # raise KeyErrorLyric
    # raise AttributeErrorLyric
    # raise ZeroDivisionErrorLyric
    # Test 5: Exception in function
    # Test 6: Exception handling in function
    # Test 7: Multiple statements in try block
    try:
        counter = counter + 1
        counter = counter + 1
    catch:
        counter = counter + 10
    finally:
        counter = counter + 100
    fade
    # Test 8: Exception with method calls
    # Test 9: Exception with built-in functions
    try:
    catch:
        print("Caught append error")
    fade
    # Test 10: Exception with indexing
    try:
    catch:
        print("Caught index error")
    fade
}
