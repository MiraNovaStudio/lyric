def square(int n) {
    return n * n
}

def greet_user(str name, int times) {
    given i in range(times)
        print("Hello,", name)
    done
}

def main() {
    print("5 squared =", square(5))
    print("Greeting Bob 3 times:")
    greet_user("Bob", 3)
}
