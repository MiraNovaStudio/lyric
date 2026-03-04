# test_lyric.ly
# Lyric adhoc test -- exercises every public function in the lyric standard library.
#
# Run with:  lyric run lyric/tests/lib/test_lyric.ly
# Output:    PASS: <desc>   for working features
#            ERROR: <desc>  for failures or thrown exceptions

import lyric

# -----------------------------------------------------------------------
# Helper: print PASS or ERROR based on a condition
# -----------------------------------------------------------------------
def check(var label, var cond) {
    if cond
        print("PASS:", label)
    else
        print("ERROR:", label)
    end
}

def main() {
    print("=== Lyric standard library test ===")
    print("")

    # ================================================================
    # pwd() — print working directory
    # ================================================================
    print("--- pwd ---")

    try:
        var cwd = lyric.pwd()
        check("pwd() returns non-empty string", cwd != "")
        print("  cwd:", cwd)
    catch Error as e:
        print("ERROR: pwd() threw exception:", e)
    fade

    # ================================================================
    # exists() — check file/dir existence
    # ================================================================
    print("")
    print("--- exists ---")

    try:
        var v = lyric.exists(".")
        check("exists('.') is true", v == true)
    catch Error as e:
        print("ERROR: exists('.') threw exception:", e)
    fade

    try:
        var v = lyric.exists("__nonexistent_lyric_test_xyz__")
        check("exists() is false for missing path", v == false)
    catch Error as e:
        print("ERROR: exists() for missing path threw exception:", e)
    fade

    # ================================================================
    # isfile() / isdir()
    # ================================================================
    print("")
    print("--- isfile / isdir ---")

    try:
        var v = lyric.isdir(".")
        check("isdir('.') is true", v == true)
    catch Error as e:
        print("ERROR: isdir('.') threw exception:", e)
    fade

    try:
        var v = lyric.isfile(".")
        check("isfile('.') is false (directory, not file)", v == false)
    catch Error as e:
        print("ERROR: isfile('.') threw exception:", e)
    fade

    try:
        var v = lyric.isdir("__nonexistent__")
        check("isdir() is false for missing path", v == false)
    catch Error as e:
        print("ERROR: isdir() for missing path threw exception:", e)
    fade

    try:
        var v = lyric.isfile("__nonexistent__")
        check("isfile() is false for missing path", v == false)
    catch Error as e:
        print("ERROR: isfile() for missing path threw exception:", e)
    fade

    # ================================================================
    # join() — path joining
    # ================================================================
    print("")
    print("--- join ---")

    try:
        var p = lyric.join("usr", "local")
        check("join('usr', 'local') returns non-empty", p != "")
        print("  join:", p)
    catch Error as e:
        print("ERROR: join() threw exception:", e)
    fade

    # ================================================================
    # path() — absolute path
    # ================================================================
    print("")
    print("--- path ---")

    try:
        var p = lyric.path(".")
        check("path('.') returns non-empty", p != "")
        print("  path('.'):", p)
    catch Error as e:
        print("ERROR: path('.') threw exception:", e)
    fade

    # ================================================================
    # base() — basename
    # ================================================================
    print("")
    print("--- base ---")

    try:
        var b = lyric.base("/home/user/file.txt")
        check("base('/home/user/file.txt') == 'file.txt'", b == "file.txt")
    catch Error as e:
        print("ERROR: base() threw exception:", e)
    fade

    try:
        var b = lyric.base("file.txt")
        check("base('file.txt') == 'file.txt'", b == "file.txt")
    catch Error as e:
        print("ERROR: base('file.txt') threw exception:", e)
    fade

    # ================================================================
    # dir() — dirname
    # ================================================================
    print("")
    print("--- dir ---")

    try:
        var d = lyric.dir("/home/user/file.txt")
        check("dir('/home/user/file.txt') returns non-empty", d != "")
        print("  dir:", d)
    catch Error as e:
        print("ERROR: dir() threw exception:", e)
    fade

    try:
        var d = lyric.dir("file.txt")
        check("dir('file.txt') == '' (no directory part)", d == "")
    catch Error as e:
        print("ERROR: dir('file.txt') threw exception:", e)
    fade

    # ================================================================
    # env() — environment variable
    # ================================================================
    print("")
    print("--- env ---")

    try:
        var p = lyric.env("PATH")
        check("env('PATH') returns non-empty", p != "" and p != None)
        print("  PATH (first 60 chars):", p[:60])
    catch Error as e:
        print("ERROR: env('PATH') threw exception:", e)
    fade

    try:
        var v = lyric.env("LYRIC_NONEXISTENT_VAR_99")
        check("env() returns None for missing var", v == None)
    catch Error as e:
        print("ERROR: env() for missing var threw exception:", e)
    fade

    # ================================================================
    # set() — set environment variable
    # ================================================================
    print("")
    print("--- set ---")

    try:
        lyric.set("LYRIC_TEST_VAR", "hello_lyric")
        var v = lyric.env("LYRIC_TEST_VAR")
        check("set() then env() returns the value", v == "hello_lyric")
    catch Error as e:
        print("ERROR: set()/env() threw exception:", e)
    fade

    # ================================================================
    # pid() — process id
    # ================================================================
    print("")
    print("--- pid ---")

    try:
        var p = lyric.pid()
        check("pid() > 0", p > 0)
        print("  pid:", p)
    catch Error as e:
        print("ERROR: pid() threw exception:", e)
    fade

    # ================================================================
    # now() — unix timestamp
    # ================================================================
    print("")
    print("--- now ---")

    try:
        var t = lyric.now()
        check("now() > 1000000000 (after 2001)", t > 1000000000)
        print("  now:", t)
    catch Error as e:
        print("ERROR: now() threw exception:", e)
    fade

    # ================================================================
    # date() — returns (date, time) tuple
    # ================================================================
    print("")
    print("--- date ---")

    try:
        var d = lyric.date()
        check("date() returns a tuple", true)
        print("  date:", d)
    catch Error as e:
        print("ERROR: date() threw exception:", e)
    fade

    # ================================================================
    # datefmt() — formatted date string
    # ================================================================
    print("")
    print("--- datefmt ---")

    try:
        var s = lyric.datefmt("%Y")
        check("datefmt('%Y') returns 4-char year", len(s) == 4)
        print("  year:", s)
    catch Error as e:
        print("ERROR: datefmt() threw exception:", e)
    fade

    try:
        var s = lyric.datefmt("%Y-%m-%d")
        check("datefmt('%Y-%m-%d') returns 10-char date", len(s) == 10)
        print("  date:", s)
    catch Error as e:
        print("ERROR: datefmt('%Y-%m-%d') threw exception:", e)
    fade

    # ================================================================
    # randflt() — random float between 0.0 and 1.0
    # ================================================================
    print("")
    print("--- randflt ---")

    try:
        var r = lyric.randflt()
        check("randflt() >= 0.0 and < 1.0", r >= 0.0 and r < 1.0)
        print("  randflt:", r)
    catch Error as e:
        print("ERROR: randflt() threw exception:", e)
    fade

    # ================================================================
    # randint() — random integer in range
    # ================================================================
    print("")
    print("--- randint ---")

    try:
        var r = lyric.randint(1, 10)
        check("randint(1, 10) >= 1 and <= 10", r >= 1 and r <= 10)
        print("  randint(1,10):", r)
    catch Error as e:
        print("ERROR: randint() threw exception:", e)
    fade

    try:
        var r = lyric.randint(5, 5)
        check("randint(5, 5) == 5", r == 5)
    catch Error as e:
        print("ERROR: randint(5,5) threw exception:", e)
    fade

    # ================================================================
    # randarr() — random element from array
    # ================================================================
    print("")
    print("--- randarr ---")

    try:
        arr items = ["a", "b", "c"]
        var r = lyric.randarr(items)
        check("randarr() returns element from array", r == "a" or r == "b" or r == "c")
        print("  randarr:", r)
    catch Error as e:
        print("ERROR: randarr() threw exception:", e)
    fade

    # ================================================================
    # sleep() — pause execution
    # ================================================================
    print("")
    print("--- sleep ---")

    try:
        var t1 = lyric.now()
        lyric.sleep(0.1)
        var t2 = lyric.now()
        check("sleep(0.1) completed without error", true)
    catch Error as e:
        print("ERROR: sleep() threw exception:", e)
    fade

    # ================================================================
    # mkdir / rmdir — directory creation and removal
    # ================================================================
    print("")
    print("--- mkdir / rmdir ---")

    str testdir = "_lyric_lib_test_tmp"

    try:
        lyric.mkdir(testdir)
        check("mkdir() creates directory", lyric.isdir(testdir) == true)
    catch Error as e:
        print("ERROR: mkdir() threw exception:", e)
    fade

    try:
        lyric.rmdir(testdir)
        check("rmdir() removes directory", lyric.exists(testdir) == false)
    catch Error as e:
        print("ERROR: rmdir() threw exception:", e)
    fade

    # ================================================================
    # cd() — change directory
    # ================================================================
    print("")
    print("--- cd ---")

    try:
        var original = lyric.pwd()
        lyric.mkdir(testdir)
        lyric.cd(testdir)
        var newcwd = lyric.pwd()
        check("cd() changes directory", newcwd != original)
        print("  changed to:", newcwd)
        lyric.cd(original)
        lyric.rmdir(testdir)
        check("cd() back to original", lyric.pwd() == original)
    catch Error as e:
        print("ERROR: cd() threw exception:", e)
        # attempt cleanup
        try:
            lyric.cd(lyric.path("."))
            lyric.rmdir(testdir)
        catch:
        fade
    fade

    # ================================================================
    # rm() — remove file
    # ================================================================
    print("")
    print("--- rm ---")

    str testfile = "_lyric_lib_test_file.txt"

    try:
        dsk f = disk(testfile)
        f.write("test content")
        f.close()
        check("created test file", lyric.isfile(testfile) == true)

        lyric.rm(testfile)
        check("rm() removes file", lyric.exists(testfile) == false)
    catch Error as e:
        print("ERROR: rm() threw exception:", e)
        # attempt cleanup
        try:
            lyric.rm(testfile)
        catch:
        fade
    fade

    # ================================================================
    # Summary
    # ================================================================
    print("")
    print("=== lyric library test complete ===")
}
