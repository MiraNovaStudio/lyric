def double(int x) {
    return x * 2
}

def apply(var func, int value) {
    return func(value)
}

def main() {
    var op = double
    print("Doubling 7:", apply(op, 7))
}
