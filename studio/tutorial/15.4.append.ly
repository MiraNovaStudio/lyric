def main() {
    dsk f = disk("log.txt")
    f.write("First line\n")
    f.close()

    f.append("Second line\n")
    f.append("Third line\n")

    str content = f.read()
    f.close()

    print("log.txt now contains:")
    print(content)
}
