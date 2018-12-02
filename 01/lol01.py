#!/usr/bin/python3

import sys

print("ans=0")
for line in sys.stdin.read().splitlines():
    print("ans=ans{}".format(line))
print("print(ans)")
