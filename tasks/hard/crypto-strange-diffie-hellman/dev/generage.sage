#!/usr/bin/env sage

import gmpy2


def generate_prime(bits):
    while True:
        p = int(gmpy2.next_prime(getrandbits(bits)))

        if p.bit_length() == bits:
            return p


def main():
    large_bits = 672
    small_bits = 31
    assert 1 + 3 * large_bits + small_bits == 2048

    while True:
        p1 = generate_prime(large_bits)
        p2 = generate_prime(large_bits)
        p3 = generate_prime(large_bits)
        q = generate_prime(small_bits)

        p = 2 * p1 * p2 * p3 * q + 1

        if gmpy2.is_prime(p):
            break

    pari.addprimes([p1, p2, p3, q])

    F = GF(p)
    g = F.multiplicative_generator()

    new_g = g ^ (g.multiplicative_order() // q)

    print(new_g)
    print(p)


if __name__ == '__main__':
    main()
