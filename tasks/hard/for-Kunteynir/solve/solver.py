import struct
import sys

TABLE_END = 0x748

def u64(x):
    return struct.unpack("!Q", x)[0]

def u32(x):
    return struct.unpack("!L", x)[0]

if __name__ == "__main__":
    data = open(sys.argv[1], 'rb').read()
    size = u64(data[0x10:0x18])
    table_size = u64(data[0x20:0x28])
    data_ptr = u64(data[0x28:0x30])
    out_data = list(bytes(size))
    
    chunks = {}
    i = 0x30

    while i < table_size:
        s_of = u32(data[i:i+4])
        i += 4
        e_of = u32(data[i:i+4])
        i += 4
        chunk_size = e_of - s_of

        chunks[(s_of,e_of)] = data[data_ptr:data_ptr+chunk_size]
        data_ptr += chunk_size
    
    for i in chunks:
        out_data[i[0]:i[1]] = chunks[i]

    fd = open("output.bmp", 'wb')
    fd.write(bytes(out_data))
    fd.close()