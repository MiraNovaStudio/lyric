# Test file to verify vim syntax highlighting

# Type declarations should be GREEN (including var)
var x = 5
int y = 10
str name = "test"
arr numbers = [1, 2, 3]
map data = {"key": "value"}
obj instance = MyClass()

def main() {
    # Function calls should be BLUE (Function color)
    print("Hello")                  # print( is BLUE
    print "Hello without parens"     # print with space is BLUE
    
    var result = int(x)              # int( is BLUE, var is GREEN
    var text = str(result)           # str( is BLUE, var is GREEN
    var items = arr([1, 2, 3])       # arr( is BLUE, var is GREEN
    var dict = map(items)            # map( is BLUE, var is GREEN
    
    # Type names in declarations should be GREEN
    int z = 10
    arr mylist = [1, 2, 3]
    var count = 0                    # var is GREEN
    
    # Built-in function calls should be BLUE
    range(10)
    type(x)
    regex("/pattern/")
    
    # Bare print syntax
    print "This works too"           # print with space is BLUE
}

