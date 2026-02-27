def main() {
    arr items = [10, 20, 30, 40, 50]

    print("First element (index 0):", items[0])
    print("Second element (index 1):", items[1])

    items[0] = 99
    print("After setting index 0 to 99:", items[0])

    # Slicing: items[start:stop]
    print("Slice [1:3] — elements at index 1 and 2:", items[1:3])
    print("Slice [:3] — first three elements:", items[:3])
    print("Slice [2:] — from index 2 to the end:", items[2:])
    print("Slice [::2] — every other element:", items[::2])
}
