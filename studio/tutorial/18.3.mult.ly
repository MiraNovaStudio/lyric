importpy math
importpy os
importpy datetime

def main() {
    print("sqrt(144):", math.sqrt(144))

    str cwd = os.getcwd()
    print("Current working directory:", cwd)

    var today = datetime.date.today()
    print("Today's date:", today)

    var now = datetime.datetime.now()
    print("Current year:", now.year)
    print("Current month:", now.month)
}
