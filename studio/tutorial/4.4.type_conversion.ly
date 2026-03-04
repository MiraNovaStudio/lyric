def main() {
    str s = "42"
    int n = int(s)       # "42" (string) becomes 42 (integer)
    flt f = flt(n)       # 42 (integer) becomes 42.0 (float)
    str back = str(f)    # 42.0 (float) becomes "42.0" (string)

    print("string \"42\" converted to int:", n)
    print("int 42 converted to float:", f)
    print("float 42.0 converted back to string:", back)

    god truth = god(1)
    print("god(1) — non-zero numbers are True:", truth)

    god empty = god("")
    print("god(\"\") — empty string is False:", empty)
}
