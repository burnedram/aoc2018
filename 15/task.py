#!/usr/bin/env pipenv-run

import sys
from itertools import chain
from queue import PriorityQueue
from functools import partial

ap = {'E': 3, 'G': 3}
if len(sys.argv) == 2:
    ap['E'] = int(sys.argv[1])

grid = dict()
units = dict()
for y, line in enumerate(sys.stdin.read().splitlines()):
    for x, ch in enumerate(line):
        grid[(x, y)] = ch
        if ch == 'G' or ch == 'E':
            units[(x, y)] = ('G' if ch == 'E' else 'E', ap[ch], 200)

def print_grid(grid, units):
    max_x = max(map(lambda xy: xy[0], grid))
    max_y = max(map(lambda xy: xy[1], grid))
    for y in range(max_y + 1):
        units_strs = list()
        for x in range(max_x + 1):
            print(grid[(x, y)], end="")
            if (x, y) in units:
                units_strs.append("{}({})".format(grid[(x, y)], units[(x, y)][2]))
        print("\t{}".format(", ".join(units_strs)))

def get_adjecent(xy):
    yield (xy[0], xy[1] - 1)
    yield (xy[0] - 1, xy[1])
    yield (xy[0] + 1, xy[1])
    yield (xy[0], xy[1] + 1)

def get_empty(grid, xys):
    return filter(lambda xy: grid[xy] == '.', xys)

def get_manhattan_dist(xy1, xy2):
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def get_dist(grid, xy1, xy2):
    dist = get_manhattan_dist(xy1, xy2)
    if dist <= 1:
        return 0
    consumed = set()
    consumed.add(xy1)
    q = PriorityQueue()
    q.put((get_manhattan_dist(xy1, xy2) + 0, 0, xy1))
    while not q.empty():
        mdist, steps, xy = q.get()
        for adjecent in get_empty(grid, get_adjecent(xy)):
            if adjecent in consumed:
                continue
            dist = get_manhattan_dist(adjecent, xy2)
            if dist <= 1:
                return steps + 1
            consumed.add(adjecent)
            q.put((get_manhattan_dist(adjecent, xy2) + steps + 1, steps + 1, adjecent))
    return None

def get_targets(units, unit_ch):
    return filter(lambda kv: kv[1][0] == unit_ch, units.items())

def get_attack_target(targets, xy):
    return min( \
            map( \
                lambda adjecent: (adjecent, targets[adjecent]), \
                filter(lambda adjecent: adjecent in targets, get_adjecent(xy))),
            key=lambda xyi: (xyi[1][2], (xyi[0][1], xyi[0][0])),
            default=None)

def tick(grid, units, move):
    moved_or_killed = False
    killed = set()
    for unit_xy, (target_ch, unit_ap, unit_hp) in \
            sorted(units.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        if unit_xy in killed:
            continue
        unit_ch = grid[unit_xy]
        targets = dict(get_targets(units, unit_ch))
        if not targets:
            return (moved_or_killed, False)
        attack = get_attack_target(targets, unit_xy)

        #print((unit_ch, unit_xy))
        #print("\t{}".format(targets))
        if (move or moved_or_killed) and attack is None:
            empty_adjecents = list(get_empty(grid, get_adjecent(unit_xy)))
            target = min( \
                    filter( \
                        lambda daxyxy: not daxyxy[0] is None, \
                        chain(*map( \
                            lambda xy: map(lambda axy: (get_dist(grid, axy, xy), xy, axy), empty_adjecents), \
                            targets))), \
                    key=lambda daxyxy: (daxyxy[0], (daxyxy[1][1], daxyxy[1][0]), (daxyxy[2][1], daxyxy[2][0])), \
                    default=None)
            if not target is None:
                moved_or_killed = True
                dist, target_xy, start_xy = target
                #print("\tmove {}".format((dist, target_xy, start_xy)))
                grid[unit_xy] = '.'
                grid[start_xy] = unit_ch
                del units[unit_xy]
                units[start_xy] = (target_ch, unit_ap, unit_hp)
                attack = get_attack_target(targets, start_xy)
            #else:
                #print("\tpass")

        if not attack is None:
            attack_xy, (unit_ch, attack_ap, attack_hp) = attack
            new_hp = attack_hp - unit_ap
            if new_hp <= 0:
                if target_ch == 'E' and not ap['E'] == 3:
                    print("AN ELF DIED")
                    return (moved_or_killed, False)
                moved_or_killed = True
                #print("\tkill {}".format((target_ch, attack_xy)))
                del units[attack_xy]
                grid[attack_xy] = '.'
                killed.add(attack_xy)
            else:
                #print("\tattack {}".format((target_ch, attack_xy)))
                units[attack_xy] = (unit_ch, attack_ap, new_hp)
    return (moved_or_killed, True)

print("Initially:")
print_grid(grid, units)
print()
rounds = 0
move = True
while True:
    move, run = tick(grid, units, move)
    if not run:
        break
    rounds += 1
    print("After {} rounds:".format(rounds))
    print_grid(grid, units)
    print()
print("Finally, after {} rounds, combat ends:".format(rounds))
print_grid(grid, units)
print()
total_hp = sum(map(lambda unit: unit[2], units.values()))
print("Outcome: {} * {} = {}".format(rounds, total_hp, rounds * total_hp)) 
