#!/usr/bin/python3

import sys
from models import Entry

entries = list()
for line in sys.stdin:
    entries.append(Entry(line))
entries.sort()

for entry in entries:
    print(entry)
