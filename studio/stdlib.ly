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
    
    int x = -100
    try: 
        x = lyric.cd("nonexist")
    catch RuntimeError as e:
        print "hello", x
    fade

    print lyric.pwd()

    arr file = lyric.ls(".")


    print file

    print "setting new test"
    lyric.set("new_test", "value")



}
