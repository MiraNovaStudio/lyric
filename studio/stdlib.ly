import lyric

def main() {
    print "sleeping 0.2 seconds"
    lyric.sleep(0.2)
    print ".done"

    str name = "Alice"
    int score = 42
    str output = "Player {} has {} points"

    print(output.format(name, score))


    print lyric.randint(1, 10)
    print lyric.randarr(["apple", "pear", "banana"])
    print lyric.randflt()

    try: 
        lyric.cd("nonexist")
    catch RuntimeError as e:
        print "here we go", e
        print e
    fade



}
