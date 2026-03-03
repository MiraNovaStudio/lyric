def main() {
    dsk f = disk("data.txt")
    arr numbers = [1, 2, 3, 4, 5]
    numbers ->> f
    f.close()

    # Read lines back into an array
    arr lines
    dsk reader = disk("data.txt")
    lines <- reader
    reader.close()

    print("Lines read back from file:", lines.len())
    print("First line:", lines[0])
}
