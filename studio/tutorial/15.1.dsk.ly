def main() {
    dsk f = disk("output.txt")
    f.write("Hello, file!")
    f.close()

    print("File written")
}
