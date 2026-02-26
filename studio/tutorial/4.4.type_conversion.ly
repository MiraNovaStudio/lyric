def main() {
    str s = "42"
    int n = int(s)
    flt f = flt(n)
    str back = str(f)

    print(n)     # 42
    print(f)     # 42.0
    print(back)  # 42.0

    god truth = god(1)
    print(truth)  # True

    god empty = god("")
    print(empty)  # False
}
