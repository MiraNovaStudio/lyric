def main() {
    arr matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    print("Full matrix:", matrix)
    print("Row at index 1:", matrix[1])
    print("Element at row 1, column 2:", matrix[1][2])

    print("All values one by one:")
    var row
    var val
    given row in matrix
        given val in row
            print(" ", val)
        done
    done
}
