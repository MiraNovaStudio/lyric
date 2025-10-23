# ImportPy Integration Tests
# Tests the importpy functionality with various Python modules

# Basic math module test
importpy math

var r = math.sqrt(9)
print(r)        # expect 3.0 (pyobject okay with var)

var pi = math.pi
print(pi)       # expect 3.141592653589793

var sin_result = math.sin(0)
print(sin_result)  # expect 0.0

# DateTime module test
importpy datetime

var now = datetime.datetime.now()
print(now.year) # prints current year

var today = datetime.date.today()
print(today)    # prints current date

# Test chained member access
var datetime_module = datetime.datetime
var now_method = datetime_module.now
var current_time = now_method()
print(current_time.year)

# Test with multiple modules
importpy os

var current_dir = os.getcwd()
print(current_dir)

# Test error handling (this should work without errors)
var math_functions = [math.sqrt, math.sin, math.cos]
print("Math functions available")

# Test pyobject type integration
var math_obj = math
var datetime_obj = datetime
print("Objects imported successfully")

# Test function calls with pyobject parameters
def test_pyobject_param(var func, var value) {
    return func(value)
}

var result1 = test_pyobject_param(math.sqrt, 16)
print(result1)  # expect 4.0

var result2 = test_pyobject_param(math.sin, math.pi/2)
print(result2)  # expect 1.0

# Test return values
def get_math_function() {
    return math.sqrt
}

var sqrt_func = get_math_function()
var result3 = sqrt_func(25)
print(result3)  # expect 5.0

# Test nested access
var math_constants = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau
}
print(math_constants.pi)

# Test with conditional logic
if math.pi > 3:
    print("Pi is greater than 3")
else:
    print("Pi is not greater than 3")
end

# Test in loops
var i = 0
given i < 3:
    var angle = i * math.pi / 2
    var sin_val = math.sin(angle)
    print(sin_val)
    i = i + 1
done

print("All importpy tests completed successfully!")
