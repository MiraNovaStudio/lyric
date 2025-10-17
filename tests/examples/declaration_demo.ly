# Demo script for strict variable declaration enforcement.
# This demonstrates the new declaration syntax in Lyric.

def main() {
    # Valid declarations with assignment
    int x = 10
    str name = "Aeonath"
    bool is_active = true
    var count = 5
    
    print("Declared variables:")
    print("x =", x)
    print("name =", name)
    print("is_active =", is_active)
    print("count =", count)
    
    # Valid declarations without assignment
    int y
    str greeting
    y = 20
    greeting = "Hello, Lyric!"
    
    print("\nAssigned after declaration:")
    print("y =", y)
    print("greeting =", greeting)
    
    # Type enforcement - this should work
    count = "now a string"
    print("\nVar can change types:")
    print("count =", count)
    
    # Assignment to declared variable
    x = 30
    print("\nReassignment:")
    print("x =", x)
}

main()
