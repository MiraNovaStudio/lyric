# Exception Handling Tests for Sprint 3
# Tests try/catch/finally blocks and raise statements

# Test 1: Basic try/catch
try:
    var result = 10 / 0
catch:
    print("Caught division by zero error")
fade

# Test 2: Try/catch with finally
var cleanup_done = False
try:
    var result = 10 / 2
    print("Division successful:", result)
catch:
    print("Caught an error")
finally:
    cleanup_done = True
    print("Cleanup completed")
fade

# Test 3: Try/catch with variable access
var x = 10
try:
    var y = x / 0
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
def risky_function(int divisor) {
    if divisor == 0:
        raise ZeroDivisionErrorLyric
    end
    return 10 / divisor
}
# Test 6: Exception handling in function
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
# Test 7: Multiple statements in try block
var counter = 0
try:
    counter = counter + 1
    var result = 10 / 0
    counter = counter + 1
catch:
    counter = counter + 10
finally:
    counter = counter + 100
fade

# Test 8: Exception with method calls
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
var result = calc.divide(10, 0)

# Test 9: Exception with built-in functions
try:
    var result = append("not_a_list", 5)
catch:
    print("Caught append error")
fade

# Test 10: Exception with indexing
try:
    var numbers = [1, 2, 3]
    var result = numbers[10]
catch:
    print("Caught index error")
fade
