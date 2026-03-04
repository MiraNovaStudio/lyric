def read_config(str path) {
    dsk f = disk(path)
    try:
        str content = f.read()
        print("Config loaded:", content)
    catch:
        print("Could not read config file:", path)
    finally:
        f.close()
        print("File handle closed")
    fade
}

def main() {
    read_config("settings.txt")
}
