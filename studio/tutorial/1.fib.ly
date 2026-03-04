# Define a function to calculate fibonacci numbers
def fib(int n) {
    if n <= 1 
        return n
    end
    return fib(n - 1) + fib(n - 2)
}

def main() {
    int result = fib(10)
    print("The 10th fibonacci number is: ", result)
}    
