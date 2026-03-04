def main() {
    str first = "Hello"
    str second = "World"

    # Concatenation
    str full = first + ", " + second + "!"
    print("Concatenated:", full)

    # Repetition
    str border = "=" * 30
    print("\"=\" repeated 30 times:", border)

    # Indexing and slicing
    str text = "Lyric"
    print("text =", text)
    print("First character (index 0):", text[0])
    print("Last character (index -1):", text[-1])
    print("Slice [1:3]:", text[1:3])
    print("Slice [:3]:", text[:3])
}
