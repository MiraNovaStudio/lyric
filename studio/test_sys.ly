importpy sys

def main () {
    var exe = sys.executable


    print ("Python executable: ", exe)

    print "Platform: " + sys.platform

    #print "Version: " + str(sys.version_info)
    #print "Module search paths:"

    int i = 0
    given i < len(sys.path):
        print sys.path[i]
        i = i + 1
    done
}
