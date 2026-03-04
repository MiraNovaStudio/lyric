int factorial(int n) {
    if n <= 1
        return 1
    end
    return n * factorial(n - 1)
}

def main() {
    print("5! (5 factorial) =", factorial(5))
    print("10! (10 factorial) =", factorial(10))
}
