from hashlib import blake2b
import string
import sys

c = [31, 132, 106, 127, 132, 177, 213, 118, 196, 119, 87, 127, 241, 63, 138, 127, 250, 127, 170, 177, 63, 177, 231, 221, 241, 177, 138, 63, 170, 41, 119, 118, 50, 87, 63, 170, 87, 127, 241, 221, 170, 196, 250, 127, 231, 170, 241, 226]

# ptzctf{3759c0a8c2cefaf4d0f8aeb5369ae9c0de72c4e0}
def check(flag):
    if len(flag) != 48:
        print("[-] Invalid flag!")
        sys.exit(0)

    alph = 'ptzctfabcdef' + "}{" + string.digits
    for i in flag:
        if i not in alph:
            print("[-] Invalid flag!")
            sys.exit(0)
        
    a = []
    for i in flag:
        a.append(int(blake2b(i.encode()).hexdigest()[2:4], 16))

        
    for i in range(len(a)):
        if c[i] != a[i]:
            print("[-] Incorrect!")
            sys.exit(-1)
    
    print("[+] Correct!")