#!/usr/bin/env python3

import os
import sys
import cmd

from Crypto.Cipher import AES  # pycryptodome


FLAG = os.getenv('FLAG', 'ptzctf{****************}').encode()
assert len(FLAG) == 24 and FLAG.startswith(b'ptzctf{') and FLAG.endswith(b'}')


class IO(cmd.Cmd):
    intro = 'Welcome to eye-yes challenge. Type help or ? to list commands.\n'
    prompt = '> '

    def onecmd(self, line: str):
        line = line.lower()

        if line == 'eof':
            sys.exit(0)

        try:
            return super().onecmd(line)
        except Exception as e:
            return print(f'ERROR: {e}')

    def do_encrypt(self, data: str):
        'Encrypt a message:  ENCRYPT <hex message>'

        cipher = self._generate_cipher()

        plaintext = bytes.fromhex(data)
        ciphertext = cipher.encrypt(plaintext)

        print(ciphertext.hex())

    def do_decrypt(self, data: str):
        'Decrypt a message:  DECRYPT <hex message>'

        cipher = self._generate_cipher()

        ciphertext = bytes.fromhex(data)
        plaintext = cipher.decrypt(ciphertext)

        print(plaintext.hex())

    def _generate_cipher(self):
        key = FLAG[len(b'ptzctf{') : -len(b'}')]
        cipher = AES.new(mode = AES.MODE_CBC, key = key, iv = key)

        return cipher


def main():
    io = IO()
    io.cmdloop()


if __name__ == '__main__':
    main()
