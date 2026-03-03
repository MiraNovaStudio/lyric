def main() {
    dsk f = disk("temp.txt")

    # Check existence
    print("Exists before write:", f.exists())

    f.write("some data")
    f.close()

    print("Exists after write:", f.exists())

    # File size in bytes
    print("File size:", f.size(), "bytes")

    # Copy and move
    f.copy("temp_copy.txt")
    f.move("temp_renamed.txt")

    # Delete
    dsk copy = disk("temp_copy.txt")
    copy.delete()

    dsk renamed = disk("temp_renamed.txt")
    renamed.delete()

    print("Cleaned up — both files deleted")
}

