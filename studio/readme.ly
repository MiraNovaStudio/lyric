# Functions with typed parameters
def greet(str name) {
    print "hello, " + name
}

def main() {
    greet("world")

    # Typed and untyped variables
    int count = 10
    str label = "items"
    var anything = [1, "two", 3.0]

    # Control flow
    if count > 5
        print "many " + label
    end

    for int i in range(count)
        print i
    done

    # Exception handling
    try:
        int result = int("not a number")
    catch ValueError as e :
        print "caught: " + str(e)
    fade
}
