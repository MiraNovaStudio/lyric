def main() {
    god a       = getopts("a", None)           # -a only, boolean
    god verbose = getopts("v", "verbose")       # -v or --verbose, boolean
    var output  = getopts("o:", "output:")       # -o file or --output=file, expects value
    god x       = getopts("x", None)            # -x only, boolean

    print("a:", a)
    print("verbose:", verbose)
    print("output:", output)
    print("x:", x)
}

