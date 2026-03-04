def main() {
    dsk f = disk("output.txt")
    str content = f.read()
    f.close()

    print("Contents of output.txt:")
    print(content)
}
