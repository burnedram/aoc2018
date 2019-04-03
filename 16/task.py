#!/usr/bin/env pipenv-run
import sys
from parse import parse
from collections import defaultdict

all_ops = dict()
def operand(func):
    all_ops[func.__name__] = func
    return func

@operand
def addr(registers, A, B, C):
    registers[C] = registers[A] + registers[B]

@operand
def addi(registers, A, B, C):
    registers[C] = registers[A] + B

@operand
def mulr(registers, A, B, C):
    registers[C] = registers[A] * registers[B]

@operand
def muli(registers, A, B, C):
    registers[C] = registers[A] * B

@operand
def banr(registers, A, B, C):
    registers[C] = registers[A] & registers[B]

@operand
def bani(registers, A, B, C):
    registers[C] = registers[A] & B

@operand
def borr(registers, A, B, C):
    registers[C] = registers[A] | registers[B]

@operand
def bori(registers, A, B, C):
    registers[C] = registers[A] | B

@operand
def setr(registers, A, B, C):
    registers[C] = registers[A]

@operand
def seti(registers, A, B, C):
    registers[C] = A

@operand
def gtir(registers, A, B, C):
    registers[C] = 1 if A > registers[B] else 0

@operand
def gtri(registers, A, B, C):
    registers[C] = 1 if registers[A] > B else 0

@operand
def gtrr(registers, A, B, C):
    registers[C] = 1 if registers[A] > registers[B] else 0

@operand
def eqir(registers, A, B, C):
    registers[C] = 1 if A == registers[B] else 0

@operand
def eqri(registers, A, B, C):
    registers[C] = 1 if registers[A] == B else 0

@operand
def eqrr(registers, A, B, C):
    registers[C] = 1 if registers[A] == registers[B] else 0

last_line_empty = False
before = None
after = None
instructions = None
possible_ops = defaultdict(lambda: set(all_ops.keys()))
total_same = 0
for line in sys.stdin:
    if not line.strip():
        if last_line_empty:
            break
        last_line_empty = True
        continue
    last_line_empty = False
    if line.startswith('Before'):
        before = list(map(int, parse('Before: [{}]', line)[0].split(', ')))
    elif line.startswith('After'):
        after = list(map(int, parse('After:  [{}]', line)[0].split(', ')))
        possible = set()
        same = 0
        for op in all_ops.values():
            registers = before.copy()
            op(registers, *instructions[1:])
            if registers == after:
                same = same + 1
                possible.add(op.__name__)
        if same >= 3:
            total_same = total_same + 1
        possible_ops[instructions[0]].intersection_update(possible)
    else:
        instructions = list(map(int, line.split(' ')))

print('Task 01: {}'.format(total_same))

actual_ops = dict()
while True:
    op = next((op for op in possible_ops.keys() if len(possible_ops[op]) == 1), None)
    if op is None:
        if possible_ops:
            print('Unable to determine all op codes')
            exit()
        break
    op_name = possible_ops[op].pop()
    del possible_ops[op]
    actual_ops[op] = all_ops[op_name]
    for op in possible_ops.keys():
        possible_ops[op].discard(op_name)

registers = defaultdict(int)
for line in sys.stdin:
    if not line.strip():
        continue
    instructions = list(map(int, line.split(' ')))
    actual_ops[instructions[0]](registers, *instructions[1:])

print('Task 02: {}'.format(registers[0]))
