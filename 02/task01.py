#!/usr/bin/python3

import sys
from collections import Counter

ans2 = 0
ans3 = 0
for line in sys.stdin.read().splitlines():
    c = Counter(line)
    has2 = False
    has3 = False
    for (key, value) in c.items():
        if not has2 and value == 2:
            has2 = True
            ans2 += 1
            if has3:
                break
        elif not has3 and value == 3:
            has3 = True
            ans3 += 1
            if has2:
                break
print(ans2 * ans3)
