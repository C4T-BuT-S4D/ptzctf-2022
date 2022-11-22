#!/usr/bin/env python3

import os
import random

from Crypto.Util.number import isPrime  # pycryptodome


FLAG = os.getenv('FLAG', 'ptzctf{***************}').encode()
assert len(FLAG) == 23 and FLAG.startswith(b'ptzctf{') and FLAG.endswith(b'}')


def generate_prime(bits):
    while True:
        rnd = random.getrandbits(bits - 1)
        prime = rnd * 2 + 1

        if isPrime(prime):
            return prime


def main():
    e = 11

    p = generate_prime(1024)
    q = generate_prime(1024)
    n = p * q

    m = int.from_bytes(FLAG, 'big')
    c = pow(m, e, n)

    print(f'{e = }')
    print(f'{n = }')
    print(f'{c = }')


if __name__ == '__main__':
    main()
