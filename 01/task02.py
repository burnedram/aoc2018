#!/usr/bin/env pipenv-run

import sys
import itertools

freqs = set([0])
freq = 0
for line in itertools.cycle(sys.stdin):
    freq += int(line)
    if freq in freqs:
        print(freq)
        exit()
    freqs.add(freq)
