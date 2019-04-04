#!/usr/bin/env pipenv-run
import sys
from itertools import groupby
from collections import defaultdict
from tqdm import tqdm

grid = dict()

for (y, line) in enumerate(sys.stdin):
    line = line.strip()
    for (x, c) in enumerate(line):
        grid[(x, y)] = c

def print_grid(grid):
    for y, xys in groupby(grid.keys(), key=lambda xy: xy[1]):
        for xy in sorted(xys, key=lambda xy: xy[0]):
            print(grid[xy], end='')
        print()

def neighbors(grid, xy):
    (x, y) = xy
    for ny in range(y - 1, y + 2):
        for nx in range(x - 1, x + 2):
            if (nx, ny) != (x, y) and (nx, ny) in grid:
                yield grid[(nx, ny)]

def count_by_type(plots):
    grouped = groupby(sorted(plots))
    return defaultdict(int, map(lambda kv: (kv[0], sum(1 for x in kv[1])), grouped))


def do_plot(grid, xy):
    n_per_type = count_by_type(neighbors(grid, xy))
    plot = grid[xy]
    if plot == '.' and n_per_type['|'] >= 3:
        return '|'
    if plot == '|' and n_per_type['#'] >= 3:
        return '#'
    if plot == '#' and (n_per_type['#'] < 1 or n_per_type['|'] < 1):
        return '.'
    return plot

def pass_time(grid):
    new_grid = grid.copy()
    for xy in grid.keys():
        new_grid[xy] = do_plot(grid, xy)
    return new_grid

def get_state(grid):
    return hash(tuple(map(lambda kv: kv[1], sorted(grid.items(), key=lambda kv: kv[0]))))

known_states = dict()
last_state = get_state(grid)
known_states[last_state] = {
    'count': count_by_type(grid.values()),
    'next_state': None
}

def simulate(n):
    global grid
    global known_states
    global last_state
    steady_state = False
    with tqdm(total=n) as pbar:
        pbar.set_description('Simulating')
        for i in range(n):
            if known_states[last_state]['next_state'] is not None:
                last_state = known_states[last_state]['next_state']
                steady_state = True
                break
            grid = pass_time(grid)
            new_state = get_state(grid)
            known_states[last_state]['next_state'] = new_state
            if new_state in known_states:
                steady_state = True
                last_state = new_state
                break
            known_states[new_state] = {
                'count': count_by_type(grid.values()),
                'next_state': None
            }
            last_state = new_state
            pbar.update(1)
        if steady_state:
            i = i + 1
            pbar.update(1)
            pbar.set_description('Fast forwarding')
            loop_len = 1
            loop_state = last_state
            while known_states[loop_state]['next_state'] != last_state:
                loop_state = known_states[loop_state]['next_state']
                loop_len = loop_len + 1
            skip = ((n - i) // loop_len) * loop_len
            i = i + skip
            pbar.update(skip)
            for i in range(i, n):
                last_state = known_states[last_state]['next_state']
                pbar.update(1)
    return known_states[last_state]['count']

by_type = simulate(10)
print('Task 01: {}'.format(by_type['|'] * by_type['#']))

by_type = simulate(1000000000 - 10)
print('Task 02: {}'.format(by_type['|'] * by_type['#']))
