#!/usr/bin/env pipenv-run
import sys
from parse import parse
from collections import defaultdict, deque
from queue import PriorityQueue
from tqdm import tqdm

depth = None
target_x = None
target_y = None
for line in sys.stdin:
    if line.startswith('depth:'):
        depth, = parse('depth: {:d}', line)
    if line.startswith('target:'):
        target_x, target_y = parse('target: {:d},{:d}', line)

class keydefaultdict(defaultdict):
    def __missing__(self, key):
        self[key] = self.default_factory(key)
        return self[key]

def calc_geologic(x, y):
    global erosion
    global target_x
    global target_y
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    if x == target_x and y == target_y:
        return 0
    return erosion[(x - 1, y)] * erosion[(x, y - 1)]

max_x = -1
max_y = -1
def point_to_geologic(point):
    global geologic
    global erosion
    global r_type
    global target_x
    global target_y
    global max_x
    global max_y
    x, y = point
    if x > max_x:
        for cx in range(max_x + 1, x + 1):
            for cy in range(0, max_y + 1):
                geologic[(cx, cy)] = calc_geologic(cx, cy)
                _ = r_type[(cx, cy)]
        max_x = x
    if y > max_y:
        for cy in range(max_y + 1, y + 1):
            for cx in range(0, max_x + 1):
                geologic[(cx, cy)] = calc_geologic(cx, cy)
                _ = r_type[(cx, cy)]
        max_y = y
    geologic[(x, y)] = calc_geologic(x, y)
    _ = r_type[(x, y)]
    return geologic[(x, y)]

def geologic_to_erosion(point):
    global depth
    global geologic
    return (geologic[point] + depth) % 20183

def erosion_to_type(point):
    global erosion
    return erosion[point] % 3

type_to_char = {
        0: '.', # rocky
        1: '=', # wet
        2: '|', # narrow
}
def print_grid(xytool):
    global r_type
    global type_to_char
    global target_x
    global target_y
    global max_x
    global max_y
    pos_x, pos_y, tool = xytool
    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            if x == pos_x and y == pos_y:
                print('X', end='')
            elif x == 0 and y == 0:
                print('M', end='')
            elif x == target_x and y == target_y:
                print('T', end='')
            else:
                print(type_to_char[r_type[(x, y)]], end='')
        print()
    print('Equipped tool: {}'.format(tool))

geologic = keydefaultdict(point_to_geologic)
erosion = keydefaultdict(geologic_to_erosion)
r_type = keydefaultdict(erosion_to_type)

# Touch the dict, generating all needed information through keydefaultdict
_ = r_type[(target_x, target_y)]
task_01 = sum(r_type.values())

tools_by_type = {
        0: set(('torch', 'climbing gear')), # rocky
        1: set(('climbing gear', 'none')),    # wet
        2: set(('torch', 'none')),            # narrow
}
tools = set(('torch', 'climbing gear', 'none'))
def adjecents(xytool):
    global r_type
    global tools_by_type
    global tools
    x, y, tool = xytool
    if x > 0 and tool in tools_by_type[r_type[(x - 1, y)]]:
        yield ((x - 1, y, tool), 1)
    if y > 0 and tool in tools_by_type[r_type[(x, y - 1)]]:
        yield ((x, y - 1, tool), 1)
    if tool in tools_by_type[r_type[(x + 1, y)]]:
        yield ((x + 1, y, tool), 1)
    if tool in tools_by_type[r_type[(x, y + 1)]]:
        yield ((x, y + 1, tool), 1)
    for new_tool in tools:
        if tool != new_tool and new_tool in tools_by_type[r_type[(x, y)]]:
            yield ((x, y, new_tool), 7)

def heuristic(xytool):
    global target_x
    global target_y
    x, y, tool = xytool
    cost = abs(target_x - x) + abs(target_y - y)
    if tool != 'torch':
        # We must have the torch equipped at the end
        cost = cost + 7
    return cost

initial_state = (0, 0, 'torch')
target_state = (target_x, target_y, 'torch')
visited = dict()
backwards = dict()
p_queue = PriorityQueue()
p_queue.put((0 + heuristic(initial_state), 0, initial_state, None))
smallest = None
with tqdm(total=target_x + target_y + 7) as pbar:
    while not p_queue.empty():
        _, value, xytool, backxytool = p_queue.get_nowait()
        x, y, tool = xytool
        if pbar.total - heuristic(xytool) > pbar.n:
            pbar.n = pbar.total - heuristic(xytool)
            pbar.refresh()
        if xytool in visited and visited[xytool] <= value:
            continue
        visited[xytool] = value
        backwards[xytool] = backxytool
        if xytool == target_state:
            smallest = value
            break
        for axytool, adist in adjecents(xytool):
            p_queue.put((value + adist + heuristic(axytool), value + adist, axytool, xytool))

walk = target_state
walks = deque()
while walk:
    walks.appendleft(walk)
    walk = backwards[walk]

def print_change():
    global change
    global total
    global initial_print
    if change[0] > 1:
        print('Walk {} steps right'.format(abs(change[0])))
        total[0] = total[0] + abs(change[0])
    elif change[0] == 1:
        print('Walk 1 step right')
        total[0] = total[0] + abs(change[0])
    elif change[0] < -1:
        print('Walk {} steps left'.format(abs(change[0])))
        total[0] = total[0] + abs(change[0])
    elif change[0] == -1:
        print('Walk 1 step left')
        total[0] = total[0] + abs(change[0])
    elif change[1] > 1:
        print('Walk {} steps down'.format(abs(change[1])))
        total[0] = total[0] + abs(change[1])
    elif change[1] == 1:
        print('Walk 1 step down')
        total[0] = total[0] + abs(change[1])
    elif change[1] < -1:
        print('Walk {} steps up'.format(abs(change[1])))
        total[0] = total[0] + abs(change[1])
    elif change[1] == -1:
        print('Walk 1 step up')
        total[0] = total[0] + abs(change[1])
    elif initial_print and change == list(initial_state):
        print('You start at (0, 0), with the torch equipped')
    else:
        print('Equip {}'.format(change[2]))
        total[1] = total[1] + 7
    initial_print = False

walk = initial_state
dwalk = (0, 0, True)
change = list(initial_state)
total = [0, 0]
initial_print = True
for w in walks:
    dw = (w[0] - walk[0], w[1] - walk[1], w[2] == walk[2])
    if dwalk != dw:
        print_change()
        change = [0, 0, w[2]]
    change[0] = change[0] + dw[0]
    change[1] = change[1] + dw[1]
    walk = w
    dwalk = dw
print_change()
print('In total {} minutes were spent walking, and {} minutes spent changing gear'.format(*total))

print()
print('Task 01: {}'.format(task_01))
print('Task 02: {}'.format(smallest))
print()

