# Lyric Standard Library
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.
importpy os
importpy time
importpy math
importpy random
importpy datetime

# sleep for x seconds, can be 0.1
def sleep(var seconds) {
    time.sleep(seconds)
}

# return random between 0.0 and 1.0
flt randflt() {
    return random.random()
}

# return random integer between low and high
int randint(int low, int high) {
    return random.randint(low, high)
}

# return a random array element
var randarr(arr list) {
    return random.choice(list)
}

# change directory
var cd(str path) {
    os.chdir(path)
}



