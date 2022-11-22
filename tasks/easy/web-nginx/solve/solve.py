#!/usr/bin/env python3
import subprocess

table = """  61 74; 62 41; 63 4D; 64 46; 65 61; 66 45; 67 56; 68 35;
  69 6B; 6A 32; 6B 37; 6C 59; 6D 63; 6E 75; 6F 34; 70 7A;
  71 64; 72 33; 73 69; 74 51; 75 30; 76 4A; 77 52; 78 50;
  79 76; 7A 73; 41 44; 42 31; 43 77; 44 72; 45 7D; 46 78;
  47 67; 48 6E; 49 4B; 4A 4C; 4B 47; 4C 58; 4D 62; 4E 5A;
  4F 6C; 50 53; 51 42; 52 7B; 53 54; 54 6D; 55 6A; 56 66;
  57 70; 58 4E; 59 6F; 5A 36; 30 43; 31 4F; 32 48; 33 55;
  34 57; 35 71; 36 39; 37 65; 38 68; 39 49; 7B 38; 7D 79;"""
table = table.replace("\n  ", " ")
table = table.strip().strip(";")
table = table.split("; ")
table = {int(a, 16):int(b, 16) for a, b in map(str.split, table)}

r = subprocess.check_output([
  "curl", "http://localhost:8384/62d1fe64e55435079f98.txt",
  "--http1.0", "-s",
  "-H", "Host:",
  "-H", "Referer: http://omegalulz",
  "-H", "User-Agent:",
  "-H", "Authorization: Bearer 1"]
).decode()

print(r.translate(table))