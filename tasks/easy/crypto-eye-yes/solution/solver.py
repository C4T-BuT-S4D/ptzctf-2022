#!/usr/bin/env python3

import sys
import socket


HOST = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
PORT = 17171


def encrypt(io, data):
    io.write(
        b'ENCRYPT ' + data.hex().encode() + b'\n',
    )
    io.flush()

    io.read(2)

    return bytes.fromhex(
        io.readline().strip().decode(),
    )


def decrypt(io, data):
    io.write(
        b'DECRYPT ' + data.hex().encode() + b'\n',
    )
    io.flush()

    io.read(2)

    return bytes.fromhex(
        io.readline().strip().decode(),
    )


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def attack(io):
    ct = encrypt(io, b'\x00' * 32)
    pt = decrypt(io, ct[16:])

    flag = xor(ct[:16], pt)
    flag = b'ptzctf{' + flag + b'}'

    return flag


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((HOST, PORT))

    io = sock.makefile('rwb')

    try:
        io.readline()
        io.readline()

        flag = attack(io)
        print(flag)
    except Exception as e:
        print(e)
    finally:
        io.close()
        sock.close()


if __name__ == '__main__':
    main()
