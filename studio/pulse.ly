# create a pulse journal post
importpy datetime; datetime

def main() {
    str journal_dir = "content/journal"
    exec("mkdir -p " + journal_dir)

    var now = datetime.now()
    str timestamp = now.strftime("%Y%m%d_%H%M")

    

    print timestamp
}
