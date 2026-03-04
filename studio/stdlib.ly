import lyric

def main() {
    print "sleeping 2 seconds"
    lyric.sleep(2)
    print ".done"

    str name = "Alice"
    int score = 42
    str output = "Player {} has {} points"

    print(output.format(name, score))
}
