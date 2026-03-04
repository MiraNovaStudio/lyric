# a simple word count program

def main(int argc, arr argv) {
    if argc == 0 or argc > 1
        print "usage: wordcount.ly <file>"
        exit()
    end

    str filename = argv[0]

    dsk file = disk(filename)

    str text = file.read()
    file.close()

    rex pattern = regex("/\w+/")
    arr words = pattern.findall(text)

    map counts = {}

    for str word in words
        if word in counts
            counts[word] += 1
        else
            counts[word] = 1
        end
    done

    print counts
}
