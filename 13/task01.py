#!/usr/bin/python3

import sys
from functools import partial
from collections import deque

rotate_cart = dict()
rotate_cart[('^', None)] = '^'
rotate_cart[('<', None)] = '<'
rotate_cart[('v', None)] = 'v'
rotate_cart[('>', None)] = '>'

rotate_cart[('^', 'cw')] = '>'
rotate_cart[('>', 'cw')] = 'v'
rotate_cart[('v', 'cw')] = '<'
rotate_cart[('<', 'cw')] = '^'

rotate_cart[('^', 'ccw')] = '<'
rotate_cart[('<', 'ccw')] = 'v'
rotate_cart[('v', 'ccw')] = '>'
rotate_cart[('>', 'ccw')] = '^'

move_cart = dict()
move_cart['^'] = ( 0, -1)
move_cart['>'] = ( 1,  0)
move_cart['v'] = ( 0,  1)
move_cart['<'] = (-1,  0)

def get_track_in_front(grid, cart, xy):
    dx, dy = move_cart[cart]
    x, y = xy 
    return grid[(x + dx, y + dy)]

def move(rotate, xy, choices):
    dx, dy = move_cart[rotate[0]]
    x, y = xy 
    return (rotate_cart[rotate], (x + dx, y + dy))

def make_choices():
    return deque(['ccw', None, 'cw'])

def junc(cart, xy, choices):
    dx, dy = move_cart[cart]
    x, y = xy 
    choice = choices[0]
    choices.rotate(-1)
    return (rotate_cart[(cart, choice)], (x + dx, y + dy))

ops = dict()
ops[('^', '|')]  = partial(move, ('^', None))
ops[('^', '/')]  = partial(move, ('^', 'cw'))
ops[('^', '\\')] = partial(move, ('^', 'ccw'))
ops[('^', '+')]  = partial(junc, ('^'))

ops[('>', '-')]  = partial(move, ('>', None))
ops[('>', '\\')] = partial(move, ('>', 'cw'))
ops[('>', '/')]  = partial(move, ('>', 'ccw'))
ops[('>', '+')]  = partial(junc, ('>'))

ops[('v', '|')]  = partial(move, ('v', None))
ops[('v', '/')]  = partial(move, ('v', 'cw'))
ops[('v', '\\')] = partial(move, ('v', 'ccw'))
ops[('v', '+')]  = partial(junc, ('v'))

ops[('<', '-')]  = partial(move, ('<', None))
ops[('<', '\\')] = partial(move, ('<', 'cw'))
ops[('<', '/')]  = partial(move, ('<', 'ccw'))
ops[('<', '+')]  = partial(junc, ('<'))

grid = dict()
carts = dict()
for y, line in enumerate(sys.stdin.read().splitlines()):
    for x, ch in enumerate(line):
        if ch == ' ':
            continue
        if ch == '^' or ch == 'v':
            carts[(x, y)] = (ch, make_choices())
            ch = '|'
        elif ch == '<' or ch == '>':
            carts[(x, y)] = (ch, make_choices())
            ch = '-'
        grid[(x, y)] = ch

def print_grid(grid, carts):
    max_x = max(map(lambda xy: xy[0], grid))
    max_y = max(map(lambda xy: xy[1], grid))
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in carts:
                print(carts[(x, y)][0], end="")
            elif (x, y) in grid:
                print(grid[(x, y)], end="")
            else:
                print(" ", end="")
        print()

def tick(grid, carts):
    for cart_xy in sorted(carts, key=lambda xy: (xy[1], xy[0])):
        cart, choices = carts[cart_xy]
        del carts[cart_xy]
        in_front = get_track_in_front(grid, cart, cart_xy)
        new_cart, new_xy = ops[(cart, in_front)](cart_xy, choices)
        if new_xy in carts:
            carts[new_xy] = ('X', choices)
            return new_xy
        else:
            carts[new_xy] = (new_cart, choices)
    return None

#print_grid(grid, carts)
crash = None
while crash is None:
    crash = tick(grid, carts)
    #print_grid(grid, carts)
print(crash)
