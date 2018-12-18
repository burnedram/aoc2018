#!/usr/bin/env pipenv-run

import sys
from collections import defaultdict

combos = defaultdict(set)
for line in sys.stdin.read().splitlines():
    for i in range(len(line)):
        trunc = line[:i] + line[i+1:]
        if trunc in combos[i]:
            print(trunc)
            exit()
        combos[i].add(trunc)
