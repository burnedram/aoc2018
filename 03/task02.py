#!/usr/bin/python3

import sys
from parse import parse
from collections import defaultdict

class Claim:
    def __init__(self, line):
        (self.id, self.x, self.y, self.w, self.h) = map(int, parse("#{} @ {},{}: {}x{}", line))

    def __str__(self):
        return "#{} @ {},{}: {}x{}".format(self.id, self.x, self.y, self.w, self.h)

land = defaultdict(list)
untainted = set()
tainted = set()
for line in sys.stdin:
    claim = Claim(line)
    for y in range(claim.y, claim.y + claim.h):
        for x in range(claim.x, claim.x + claim.w):
            claims = land[(x, y)]
            claims.append(claim)
            if len(claims) < 2:
                if not claim.id in tainted:
                    untainted.add(claim.id)
            else:
                for claim in claims:
                    tainted.add(claim.id)
                    if claim.id in untainted:
                        untainted.remove(claim.id)

print(untainted)
