def main() {
    print("Testing nested control flow...")
    
    # Test nested if statements
    x = 5
    if x > 3:
        print("x is greater than 3")
        if x < 10:
            print("x is also less than 10")
        else:
            print("x is not less than 10")
    else:
        print("x is not greater than 3")
    end
    
    # Test nested given loops
    given i in range(3):
        print("Outer loop:", i)
        given j in range(2):
            print("  Inner loop:", j)
        done
    done
    
    # Test if inside given
    given num in range(5):
        if num > 2:
            print("Number", num, "is greater than 2")
        else:
            print("Number", num, "is not greater than 2")
        end
    done
    
    print("Nested control flow test complete!")
}
