# does_it_work.ly

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
    # Vars and (optional) explicit typing
    int x = 5
    var y = add(x, 7)
    greet("Lyric")

    print("x = ", x)
    print("y = ", y)

    # Conditionals with end
    if y > 10
        print("Branch: y > 10")
    else if y == 10
        print("Branch: y == 10")
    else
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
    #catch IndexError as e:
    #    print("Caught IndexError: " + e)
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

    print("All constructs exercised. ✅")
}
