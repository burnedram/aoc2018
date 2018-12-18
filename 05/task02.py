#!/usr/bin/env pipenv-run

import sys
from models import UnitNode

head = None
tail = head
for line in sys.stdin.read().splitlines():
    for unit in line:
        if head is None:
            head = tail = UnitNode(unit)
        else:
            tail = UnitNode(unit).insert_self_after(tail)

unique_units = set()
for unit in head:
    unique_units.add(unit.unit.lower())

slimmest_length = None
for unique_unit in unique_units:
    slim_head = None
    slim_tail = head
    for unit in head:
        if unit.unit.lower() == unique_unit:
            continue
        if slim_head is None:
            slim_head = slim_tail = UnitNode(unit.unit)
        elif slim_tail.unit != unit.unit and slim_tail.unit.lower() == unit.unit.lower():
            slim_tail = slim_tail.remove_self()
            if slim_tail == None:
                slim_head = None;
        else:
            slim_tail = UnitNode(unit.unit).insert_self_after(slim_tail)
    length = slim_head.get_length()
    if slimmest_length is None or length < slimmest_length:
        slimmest_length = length

print(slimmest_length)
