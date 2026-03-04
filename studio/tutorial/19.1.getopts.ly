def main() {
    god verbose = getopts("v", "verbose")    # no colon = boolean flag
    var filename = getopts("f:", "file:")     # colon = expects a value

    if verbose
        print("Verbose mode is ON")
    end

    if filename != False
        print("Processing file:", filename)
    else
        print("No file specified")
    end
}
