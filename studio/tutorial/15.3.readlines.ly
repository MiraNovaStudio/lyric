def main() {
    dsk f = disk("output.txt")
    arr lines = f.readlines()
    f.close()
    str line

    print("Number of lines:", lines.len())
    print("Contents line by line:")
    for line in lines
        print(" >", line)
    done
}
