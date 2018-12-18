#!/usr/bin/env pipenv-run

import sys
from collections import defaultdict
from models import Claim

land = defaultdict(list)
untainted = set()
tainted = set()
for line in sys.stdin:
    claim = Claim(line)
    for y in range(claim.y, claim.y + claim.h):
        for x in range(claim.x, claim.x + claim.w):
            claims = land[(x, y)]
            claims.append(claim.id)
            if len(claims) < 2:
                if not claim.id in tainted:
                    untainted.add(claim.id)
            else:
                for claim_id in claims:
                    tainted.add(claim_id)
                    if claim_id in untainted:
                        untainted.remove(claim_id)

print(untainted)
