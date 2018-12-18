#!/usr/bin/env pipenv-run

import sys

print("ans=0")
for line in sys.stdin.read().splitlines():
    print("ans=ans{}".format(line))
print("print(ans)")
