int get_max(int a, int b) {
    if a > b
        return a
    else
        return b
    end
}

str make_label(str key, str value) {
    return key + ": " + value
}

def main() {
    int m = get_max(8, 13)
    print("The larger of 8 and 13 is:", m)
    print(make_label("Name", "Alice"))
}
