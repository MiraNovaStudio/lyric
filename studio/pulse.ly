#!/usr/bin/env lyric
# create a pulse journal post

import lyric

def main(int argc, arr argv) {
    str journal_dir = "content/journal"
    exec("mkdir -p " + journal_dir)

    str timestamp = lyric.datefmt("%Y%m%d_%H%M")

    god help = getopts("h", "help")
    god list = getopts("l", "list")

    if help 
        print "Usage: pulse.ly [options] [title]"
        print " -h --help   Show this help message"
        print " -l --list   List last five journal entries"
        exit()
    end

    if list
        str output
        exec("ls -t " + journal_dir + "/*.md") | exec("head -n 5") -> output
        print "Last 5 journal entries:"
        print output
        exit()
    end 

    if not argc
        print "Error: Please provide a title for your journal entry."
        print "Usage: pulse.ly [options] [title]"
        exit(1)
    end

    arr date = lyric.date()

    str journal_file_name = journal_dir + "/" + timestamp + "_POST.md"

    dsk journal_file = disk(journal_file_name)

    print "---" ->> journal_file
    print "title: " + (argv[0]) ->> journal_file
    print "date: " + date[0] ->> journal_file
    print "---" ->> journal_file
    print "" ->> journal_file
    print "Write your journal entry here..." ->> journal_file
    print "" ->> journal_file
    print "*-- Michael (Aeonath)*" ->> journal_file 
    print "" ->> journal_file

    print "Journal file created: " + journal_file_name
}
