#!/usr/bin/env pipenv-run

import sys
from collections import deque, defaultdict

pattern = next(sys.stdin).strip().strip('^$')

def mark_room(grid, x, y):
    grid[(x, y)] = '.'
    grid[(x + 1, y + 1)] = '#'
    grid[(x + 1, y - 1)] = '#'
    grid[(x - 1, y + 1)] = '#'
    grid[(x - 1, y - 1)] = '#'
    return grid

ops = dict()
def op(op):
    def func(func):
        ops[op] = func
        return func
    return func

@op('S')
def south(grid, q_pos, x, y):
    grid[(x, y + 1)] = '-'
    grid = mark_room(grid, x, y + 2)
    return (grid, q_pos, x, y + 2)

@op('W')
def west(grid, q_pos, x, y):
    grid[(x - 1, y)] = '|'
    grid = mark_room(grid, x - 2, y)
    return (grid, q_pos, x - 2, y)

@op('E')
def east(grid, q_pos, x, y):
    grid[(x + 1, y)] = '|'
    grid = mark_room(grid, x + 2, y)
    return (grid, q_pos, x + 2, y)

@op('N')
def north(grid, q_pos, x, y):
    grid[(x, y - 1)] = '-'
    grid = mark_room(grid, x, y - 2)
    return (grid, q_pos, x, y - 2)

@op('(')
def open_group(grid, q_pos, x, y):
    q_pos.append((x, y))
    return (grid, q_pos, x, y)

@op(')')
def close_group(grid, q_pos, x, y):
    x, y = q_pos.pop()
    return (grid, q_pos, x, y)

@op('|')
def or_group(grid, q_pos, x, y):
    x, y = q_pos[-1]
    return (grid, q_pos, x, y)

def print_grid(grid, pos_x, pos_y):
    min_x = min(map(lambda xy: xy[0], grid.keys()))
    max_x = max(map(lambda xy: xy[0], grid.keys()))
    min_y = min(map(lambda xy: xy[1], grid.keys()))
    max_y = max(map(lambda xy: xy[1], grid.keys()))
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if x == pos_x and y == pos_y:
                print('X', end='')
            elif x == 0 and y == 0:
                print('o', end='')
            elif (x, y) in grid:
                print(grid[(x, y)], end='')
            else:
                print('?', end='')
        print()

state = (
        mark_room(dict(), 0, 0),
        deque(),
        0,
        0,
)
for c in pattern:
    state = ops[c](*state)

def finalize_grid(grid):
    min_x = min(map(lambda xy: xy[0], grid.keys()))
    max_x = max(map(lambda xy: xy[0], grid.keys()))
    min_y = min(map(lambda xy: xy[1], grid.keys()))
    max_y = max(map(lambda xy: xy[1], grid.keys()))
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in grid:
                continue
            if grid.get((x - 1, y), None) == '#' and grid.get((x + 1, y), None) == '#':
                grid[(x, y)] = '#'
            elif grid.get((x, y - 1), None) == '#' and grid.get((x, y + 1), None) == '#':
                grid[(x, y)] = '#'
    return grid

grid, _, pos_x, pos_y = state
grid = finalize_grid(grid)

def walks(grid, x, y):
    if grid.get((x - 1, y), None) == '|':
        yield (x - 2, y)
    if grid.get((x + 1, y), None) == '|':
        yield (x + 2, y)
    if grid.get((x, y - 1), None) == '-':
        yield (x, y - 2)
    if grid.get((x, y + 1), None) == '-':
        yield (x, y + 2)

backwards = dict()
backwards[(0, 0)] = None
q = deque()
q.appendleft((0, 0))
while q:
    x, y = q.pop()
    for wx, wy in walks(grid, x, y):
        if (wx, wy) not in backwards:
            backwards[(wx, wy)] = (x, y)
            q.appendleft((wx, wy))

forwards = defaultdict(set)
for p in backwards:
    forwards[backwards[p]].add(p)
del forwards[None]

lengths = dict()
lengths[(0, 0)] = 0
q = deque()
q.appendleft((0, 0))
while q:
    x, y = q.pop()
    for wx, wy in forwards[(x, y)]:
        lengths[(wx, wy)] = lengths[(x, y)] + 1
        q.appendleft((wx, wy))

print('Task 01: {}'.format(max(lengths.values())))
print('Task 02: {}'.format(sum(1 if l >= 1000 else 0 for l in lengths.values())))
