import os

os.system("xxd -r hd.txt > out.bin")
fd = open("arch.7z", 'wb')
fd.write(open('out.bin', 'rb').read()[::-1])
fd.close()
os.system("7z e arch.7z")

buf = open('image.png', 'rb').read()
out = buf[:0x16]
out += b'\x01\xff'
out += buf[0x18:]
fd = open('image_fix.png', 'wb')
fd.write(out)
fd.close()
