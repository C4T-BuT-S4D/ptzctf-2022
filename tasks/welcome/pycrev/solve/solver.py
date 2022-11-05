#!/usr/bin/env python3
from hashlib import blake2b
import string
# use https://www.toolnb.com/tools-lang-en/pyc.html to decopile
c = [31, 132, 106, 127, 132, 177, 213, 118, 196, 119, 87, 127, 241, 63, 138, 127, 250, 127, 170, 177, 63, 177, 231, 221, 241, 177, 138, 63, 170, 41, 119, 118, 50, 87, 63, 170, 87, 127, 241, 221, 170, 196, 250, 127, 231, 170, 241, 226]


if __name__ == "__main__":
    map_ = {}
    alph = 'ptzctfabcdef' + "}{" + string.digits

    for i in alph:
        map_[int(blake2b(i.encode()).hexdigest()[2:4], 16)] = i
    
    for i in c:
        print(map_[i], end='')
    