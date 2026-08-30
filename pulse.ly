#!/usr/bin/env lyric

import lyric

def main(int argc, arr argv) {
    str journal_file_name = "test.txt"

    dsk journal_file = disk(journal_file_name)

    print "— MiraNova Studios" ->> journal_file 

    print "Journal file created: " + journal_file_name
}
