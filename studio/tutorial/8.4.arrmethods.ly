def main() {
    arr nums = [3, 1, 4, 1, 5, 9, 2, 6]
    print("Starting array:", nums)
    print("Length:", nums.len())

    nums.append(7)
    print("After append(7):", nums)

    int last = nums.pop()
    print("Popped last element:", last)
    print("Array after pop:", nums)

    nums.remove(1)
    print("After removing first 1:", nums)

    nums.sort()
    print("After sort:", nums)

    nums.reverse()
    print("After reverse:", nums)

    print("Count of value 1 in array:", nums.count(1))
    print("Index of value 5:", nums.index(5))

    nums.insert(0, 0)
    print("After insert(0, 0) — added 0 at the front:", nums)

    print("Minimum value:", nums.min())
    print("Maximum value:", nums.max())
    print("Sum of all values:", nums.sum())

    arr copy = nums.copy()
    copy.clear()
    print("Cleared copy — length is now:", copy.len())
}
