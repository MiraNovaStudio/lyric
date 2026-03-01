def main() {
    # Count from 0 to 4
    print("Counting from 0 to 4:")
    int i
    given i in range(5)
        print(" ", i)
    done

    # Iterate over an array
    arr colors = ["red", "green", "blue"]
    print("Available colors:")
    var color
    for color in colors
        print(" -", color)
    done
}
