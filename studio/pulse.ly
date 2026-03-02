# create a pulse journal post
importpy datetime; datetime

def main() {
    var now = datetime.now()
    str timestamp = now.strftime("%Y%m%d_%H%M")


    print timestamp
}
