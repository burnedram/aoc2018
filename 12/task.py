#!/usr/bin/python3

import sys
from parse import parse
from collections import defaultdict
import itertools

if len(sys.argv) > 2:
    print("Usage: {} MAX".format(sys.argv[0]))
    print("\t MAX: (optional) max evolutions to simulate")
    exit(1)

evos = None
if len(sys.argv) == 2:
    evos = int(sys.argv[1])

def convert_state(pot):
    return pot == '#'

state = set()
for i, pot in enumerate(parse("initial state: {}", next(sys.stdin))[0]):
    if convert_state(pot):
        state.add(i)
next(sys.stdin)

def print_state(state):
    print("{}\t: ".format(min(state)), end="")
    for i in range(min(state), max(state) + 1):
        print('#' if i in state else '.', end="")
    print()
print("0\t", end="")
print_state(state)

def middle_out(left, right):
    middle = (right - left) // 2
    yield (left + middle, left + middle)
    for i in range(1, middle + 1):
        yield (left + middle - i, left + middle + i)

nested_dict = lambda: defaultdict(nested_dict)
rules = nested_dict()
for line in sys.stdin:
    rule_str, result = parse("{} => {}", line)
    rule = rules
    for left, right in middle_out(0, len(rule_str)):
        rule = rule[(convert_state(rule_str[left]), convert_state(rule_str[right]))]
    rule["result"] = convert_state(result)

def evolve(state, rules, i):
    rule = rules
    for left, right in middle_out(i - 2, i + 3):
        rule = rule[(left in state, right in state)]
    return "result" in rule and rule["result"]

min_old = min(state)
norm = set(map(lambda x: x - min_old, state))
for state_idx in range(1, evos + 1) if not evos is None else itertools.count(1):
    new_state = set()
    for i in range(min(state) - 1, max(state) + 2):
        if evolve(state, rules, i):
            new_state.add(i)
    print("{}\t".format(state_idx), end="")
    print_state(new_state)
    min_new = min(new_state)
    norm_new = set(map(lambda x: x - min_new, new_state))
    if norm == norm_new:
        state_idx -= 1
        break;
    state = new_state
    norm = norm_new

extra = len(state) * (evos - state_idx) if not evos is None else 0
print(sum(state) + extra)
