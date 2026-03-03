def main() {
    dsk myfile = disk("notes.txt")

    # Overwrite the file
    str line1 = "First note"
    print line1 -> myfile

    # Append to the file
    str line2 = "Second note"
    print line2 ->> myfile

    str line3 = "Third note"
    print line3 ->> myfile

    myfile.close()

    # Read everything back
    str content
    dsk reader = disk("notes.txt")
    content <- reader
    reader.close()

    print("notes.txt contains:")
    print(content)
}
