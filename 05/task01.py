#!/usr/bin/env pipenv-run

import sys
from models import UnitNode

head = None
tail = head
for line in sys.stdin.read().splitlines():
    for unit in line:
        if head is None:
            head = tail = UnitNode(unit)
        elif tail.unit != unit and tail.unit.lower() == unit.lower():
            tail = tail.remove_self()
            if tail == None:
                head = None;
        else:
            tail = UnitNode(unit).insert_self_after(tail)

for unit in head:
    print(unit.unit, end="")
