def main() {
    print("Testing nested control flow...")
    
    # Test 1: if inside given loop
    given i in range(3):
        if i > 1:
            print("i is greater than 1:", i)
        else:
            print("i is 1 or less:", i)
        end
    done
    
    print("---")
    
    # Test 2: given loop inside if
    x = 5
    if x > 3:
        print("x is greater than 3, counting down:")
        given j in range(x):
            print("Count:", j)
        done
    else:
        print("x is 3 or less")
    end
    
    print("---")
    
    # Test 3: nested if statements
    y = 2
    if y > 0:
        print("y is positive")
        if y > 1:
            print("y is greater than 1")
            if y > 2:
                print("y is greater than 2")
            else:
                print("y is exactly 2")
            end
        else:
            print("y is exactly 1")
        end
    else:
        print("y is not positive")
    end
    
    print("---")
    
    # Test 4: nested given loops
    print("Nested loops:")
    given outer in range(2):
        given inner in range(3):
            print("outer:", outer, "inner:", inner)
        done
    done
}
