#!/usr/bin/python3

import sys
from collections import defaultdict
from models import Claim

land = defaultdict(int)
for line in sys.stdin:
    claim = Claim(line)
    for y in range(claim.y, claim.y + claim.h):
        for x in range(claim.x, claim.x + claim.w):
            land[(x, y)] += 1

print(sum(map(lambda x: 0 if x < 2 else 1, land.values())))
