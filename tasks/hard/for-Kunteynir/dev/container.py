import struct
import sys
import random

def p64(x):
    return struct.pack("!Q", x)

def p32(x):
    return struct.pack("!L", x)

if __name__ == "__main__":
    data = open(sys.argv[1], 'rb').read()
    blocks = {}

    i = 0
    while i < len(data):
        s_of = i
        e_of = i + random.randint(0x100, 0x1000)
        
        if e_of > len(data):
            e_of = len(data)

        blocks[(s_of, e_of)] = data[s_of:e_of]
        
        i = e_of
    
    header = b'KEK_FORMAT' + b'\x00' * 6
    header += p64(len(data)) + p64(0x0)

    keys = list(blocks.keys())
    random.shuffle(keys)

    table = b''
    out_data = b''

    for i in keys:
        table += p32(i[0]) + p32(i[1])
    
    for i in keys:
        out_data += blocks[i]

    fd = open("out.bin", 'wb')
    fd.write(header + p64(len(table)) + p64(len(header)+len(table) + 16) + table + out_data)
    fd.close()