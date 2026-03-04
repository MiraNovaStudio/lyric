def main() {
    var infile  = getopts("i:", "input:")
    var outfile = getopts("o:", "output:")
    god verbose = getopts("v", "verbose")

    if infile == False
        print("Usage: lyric program.ly --input=file.txt [--output=out.txt] [-v]")
        exit(1)
    end

    if verbose
        print("Reading from:", infile)
    end

    str content
    dsk reader = disk(infile)
    content <- reader
    reader.close()

    if outfile != False
        if verbose
            print("Writing to:", outfile)
        end
        str result = "Processed: " + content
        dsk writer = disk(outfile)
        result -> writer
        writer.close()
        print("Done!")
    else
        print(content)
    end
}
