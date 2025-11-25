# Test file to verify vim syntax highlighting

# Type declarations should be GREEN
int x = 5
str name = "test"
arr numbers = [1, 2, 3]
map data = {"key": "value"}
obj instance = MyClass()

def main() {
    # Function calls should be BLUE (Function color)
    print("Hello")
    var result = int(x)
    var text = str(result)
    var items = arr([1, 2, 3])
    var dict = map(items)
    
    # Type names in declarations should be GREEN
    int y = 10
    arr mylist = [1, 2, 3]
    
    # Built-in function calls should be BLUE
    range(10)
    type(x)
    regex("/pattern/")
}

