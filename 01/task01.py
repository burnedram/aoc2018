#!/usr/bin/env pipenv-run

import sys

freq = 0
for line in sys.stdin:
    freq += int(line)
print(freq)
