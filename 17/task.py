#!/usr/bin/env pipenv-run
import sys
from parse import parse
from collections import defaultdict, deque

grid = defaultdict(lambda: '.')

min_x = None
min_y = None
max_x = None
max_y = None
for line in sys.stdin:
    (a, xy, b, left, right) = parse('{}={:d}, {}={:d}..{:d}', line)
    if a == 'x':
        if min_x is None or xy < min_x:
            min_x = xy
        if max_x is None or xy > max_x:
            max_x = xy
        if min_y is None or left < min_y:
            min_y = left
        if max_y is None or right > max_y:
            max_y = right
        for y in range(left, right + 1):
            grid[(xy, y)] = '#'
    else:
        if min_y is None or xy < min_y:
            min_y = xy
        if max_y is None or xy > max_y:
            max_y = xy
        if min_x is None or left < min_x:
            min_x = left
        if max_x is None or right > max_x:
            max_x = right
        for x in range(left, right + 1):
            grid[(x, xy)] = '#'

min_x = min_x - 1
max_x = max_x + 1

spring_x = 500
spring_y = min_y - 1

def print_grid():
    for x in range(min_x, max_x + 1):
        print('+' if x == spring_x else '.', end='')
    print()
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(grid[(x, y)], end='')
        print()
    print()

still_q = deque()
flow_q = deque()
flow_q.append((spring_x, spring_y + 1))
grid[(spring_x, spring_y + 1)] = '|'
while flow_q:
    added = False
    (x, y) = flow_q.pop()
    if y + 1 <= max_y and grid[(x, y + 1)] == '.':
        if not added:
            flow_q.append((x, y))
            added = True
        flow_q.append((x, y + 1))
        grid[(x, y + 1)] = '|'

    if grid[(x, y + 1)] == '#' or grid[(x, y + 1)] == '~':
        flowing = False
        if x + 1 <= max_x and grid[(x + 1, y)] == '.':
            if not added:
                flow_q.append((x, y))
                added = True
            flow_q.append((x + 1, y))
            grid[(x + 1, y)] = '|'
            flowing = True
        if x - 1 >= min_x and grid[(x - 1, y)] == '.':
            if not added:
                flow_q.append((x, y))
                added = True
            flow_q.append((x - 1, y))
            grid[(x - 1, y)] = '|'
            flowing = True
        if not flowing:
            still_min_x = None
            still_max_x = None
            for sx in range(x, min_x - 1, -1):
                if grid[(sx, y)] == '#':
                    still_min_x = sx + 1
                    break
                if grid[(sx, y)] != '|':
                    break
                if grid[(sx, y + 1)] != '#' and grid[(sx, y + 1)] != '~':
                    break
            if still_min_x is not None:
                for sx in range(x, max_x + 1):
                    if grid[(sx, y)] == '#':
                        still_max_x = sx - 1
                        break
                    if grid[(sx, y)] != '|':
                        break
                    if grid[(sx, y + 1)] != '#' and grid[(sx, y + 1)] != '~':
                        break
                if still_max_x is not None:
                    for sx in range(still_min_x, still_max_x + 1):
                        grid[(sx, y)] = '~'

#print_grid()
print('Task 01: {}'.format(sum(map(lambda xy: 1 if xy == '|' or xy == '~' else 0, grid.values()))))
print('Task 02: {}'.format(sum(map(lambda xy: 1 if xy == '~' else 0, grid.values()))))
