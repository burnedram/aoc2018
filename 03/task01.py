#!/usr/bin/python3

import sys
from parse import parse
from collections import defaultdict

class Claim:
    def __init__(self, line):
        (self.id, self.x, self.y, self.w, self.h) = map(int, parse("#{} @ {},{}: {}x{}", line))

    def __str__(self):
        return "#{} @ {},{}: {}x{}".format(self.id, self.x, self.y, self.w, self.h)

land = defaultdict(int)
for line in sys.stdin:
    claim = Claim(line)
    for y in range(claim.y, claim.y + claim.h):
        for x in range(claim.x, claim.x + claim.w):
            land[(x, y)] += 1

print(sum(map(lambda x: 0 if x < 2 else 1, land.values())))
