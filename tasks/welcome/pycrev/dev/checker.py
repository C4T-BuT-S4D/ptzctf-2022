#!/usr/bin/env python3
from task import check
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        flag = sys.argv[1]
    else:
        print("[-] Usage: ./checker.py <flag>")
        sys.exit(-1)
    
    check(flag)