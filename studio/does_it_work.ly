# does_it_work.ly
import mathlib

# ——— Python interop (importpy) ———
importpy datetime
importpy math

# ——— Functions (typed + untyped), return statements ———
def add(int a, int b) { 
    return a + b 
}

def greet(name) { 
    print("Hello, ", name) 
}

# ——— Simple class declaration (symbolic close with +++) ———
class Example
    str name = "Guest"
    
    def hello() {
        print("Hello, ", self.name)
    }    # minimal class; parser should accept class block and +++ close
+++

# ——— Main entrypoint ———
def main() {
    greet("Lyric")
    
    # Vars and (optional) explicit typing
    int x = 5
    var y = add(x, 7)

    print("x = ", x)
    print("y = ", y)

    # Conditionals with end
    if y > 10:
        print("Branch: y > 10")
    case y == 10:
        print("Branch: y == 10")
    else:
        print("Branch: y < 10")
    end

    # given/done loop (basic iteration)
    int i = 0
    given i < 3:
        print("loop i = ", i)
        i = i + 1
    done

    # Lists and indexing (for try/catch test)
    var items = [1, 2, 3]

    # try / catch / finally / fade with IndexError branch
    try:
        var bad = items[5]      # should raise IndexError
        print("This should not print")
    catch IndexError as e:
        print("Caught IndexError: " + e)
    catch:
        print("Caught some other error")
    finally:
        print("Finally always runs")
    fade

    # importpy usage: datetime and math interop (values are internal pyobject represented as var)
    var now = datetime.datetime.now()
    print("Year from Python datetime: ", now.year)

    var radians = math.pi / 2
    var s = math.sin(radians)
    print("sin(pi/2) from Python math: ", s)

    # rex datatype usage for regex operations
    rex email_pattern = regex("/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/")
    var test_email = "user@example.com"
    
    if email_pattern.match(test_email):
        print("Valid email: " + test_email)
    else:
        print("Invalid email: " + test_email)
    end

    arr numbers = [10, 20, 30, 40, 50]
    int sum = 0
    int num
    for num in numbers:
        sum = sum + num
    done
    print sum

    map person = {"name": "Alice", "age": 30, "city": "Seattle"}
    print person["name"]
    print person["age"]
    person["occupation"] = "Engineer"
    print person["occupation"]

    int result = add(5, 7)
    print result
    Calculator calc = Calculator(10)
    calc.add(5)
    print calc.value
    int hidden = get_secret()
    print hidden
        
    # Test file i/o operator
    print("All constructs exercised. ✅")
}
