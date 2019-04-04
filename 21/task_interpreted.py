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


pc = 0
ip = None
registers = defaultdict(int)
program = list()

for line in sys.stdin:
    if line.startswith('#ip'):
        ip, = parse('#ip {:d}', line)
        continue
    program.append(tuple(parse('{} {:d} {:d} {:d}', line)))

mod_ops = dict()
def mod_operand(func):
    mod_ops[func.__name__.split('_')[1]] = func
    return func

@mod_operand
def mod_addr(ip, A, B, C):
    A = 'PC' if A == ip else 'r{}'.format(A)
    B = 'PC' if B == ip else 'r{}'.format(B)
    if C == ip:
        return 'JMP {}+{}'.format(A, B)
    return 'r{} = {}+{}'.format(C, A, B)

@mod_operand
def mod_addi(ip, A, B, C):
    A = 'PC' if A == ip else 'r{}'.format(A)
    if C == ip:
        return 'JMP {}+{}'.format(A, B)
    return 'r{} = {}+{}'.format(C, A, B)

@mod_operand
def mod_mulr(ip, A, B, C):
    A = 'PC' if A == ip else 'r{}'.format(A)
    B = 'PC' if B == ip else 'r{}'.format(B)
    if C == ip:
        return 'JMP {}*{}'.format(A, B)
    return 'r{} = {}*{}'.format(C, A, B)

@mod_operand
def mod_muli(ip, A, B, C):
    A = 'PC' if A == ip else 'r{}'.format(A)
    if C == ip:
        return 'JMP {}*{}'.format(A, B)
    return 'r{} = {}*{}'.format(C, A, B)

@mod_operand
def mod_banr(ip, A, B, C):
    A = 'PC' if A == ip else 'r{}'.format(A)
    B = 'PC' if B == ip else 'r{}'.format(B)
    if C == ip:
        return 'JMP {} & {}'.format(A, B)
    return 'r{} = {} & {}'.format(C, A, B)

@mod_operand
def mod_bani(ip, A, B, C):
    A = 'PC' if A == ip else 'r{}'.format(A)
    if C == ip:
        return 'JMP {} & {}'.format(A, B)
    return 'r{} = {} & {}'.format(C, A, B)

@mod_operand
def mod_borr(ip, A, B, C):
    A = 'PC' if A == ip else 'r{}'.format(A)
    B = 'PC' if B == ip else 'r{}'.format(B)
    if C == ip:
        return 'JMP {} | {}'.format(A, B)
    return 'r{} = {} | {}'.format(C, A, B)

@mod_operand
def mod_bori(ip, A, B, C):
    A = 'PC' if A == ip else 'r{}'.format(A)
    if C == ip:
        return 'JMP {} | {}'.format(A, B)
    return 'r{} = {} | {}'.format(C, A, B)

@mod_operand
def mod_setr(ip, A, B, C):
    A = 'PC' if A == ip else 'r{}'.format(A)
    if C == ip:
        return 'JMP {}'.format(A)
    return 'r{} = {}'.format(C, A)

@mod_operand
def mod_seti(ip, A, B, C):
    if C == ip:
        return 'JMP {}'.format(A)
    return 'r{} = {}'.format(C, A)

@mod_operand
def mod_gtir(ip, A, B, C):
    B = 'PC' if B == ip else 'r{}'.format(B)
    if C == ip:
        return 'JMP {} > {}'.format(A, B)
    return 'r{} = {} > {}'.format(C, A, B)

@mod_operand
def mod_gtri(ip, A, B, C):
    A = 'PC' if A == ip else 'r{}'.format(A)
    if C == ip:
        return 'JMP {} > {}'.format(A, B)
    return 'r{} = {} > {}'.format(C, A, B)

@mod_operand
def mod_gtrr(ip, A, B, C):
    A = 'PC' if A == ip else 'r{}'.format(A)
    B = 'PC' if B == ip else 'r{}'.format(B)
    if C == ip:
        return 'JMP {} > {}'.format(A, B)
    return 'r{} = {} > {}'.format(C, A, B)

@mod_operand
def mod_eqir(ip, A, B, C):
    B = 'PC' if B == ip else 'r{}'.format(B)
    if C == ip:
        return 'JMP {} == {}'.format(A, B)
    return 'r{} = {} == {}'.format(C, A, B)

@mod_operand
def mod_eqri(ip, A, B, C):
    A = 'PC' if A == ip else 'r{}'.format(A)
    if C == ip:
        return 'JMP {} == {}'.format(A, B)
    return 'r{} = {} == {}'.format(C, A, B)

@mod_operand
def mod_eqrr(ip, A, B, C):
    A = 'PC' if A == ip else 'r{}'.format(A)
    B = 'PC' if B == ip else 'r{}'.format(B)
    if C == ip:
        return 'JMP {} == {}'.format(A, B)
    return 'r{} = {} == {}'.format(C, A, B)

for i, ins in enumerate(program):
    print('{}: {}'.format(str(i).rjust(2, ' '), mod_ops[ins[0]](ip, *ins[1:])))
print()

def step():
    global pc
    global ip
    global registers
    global program
    if pc < 0 or pc >= len(program):
        return False
    if ip is not None:
        registers[ip] = pc
    all_ops[program[pc][0]](registers, *program[pc][1:])
    if ip is not None:
        pc = registers[ip]
    pc = pc + 1
    return True

# On line 28, the program halts if r0 == r3
halt_pc = 28
halt_r = 3
while step():
    if pc == halt_pc:
        break
print('Task 01: {}'.format(registers[halt_r]))
print()

def get_state():
    global pc
    global registers
    return hash((pc, *registers))

print('WARNING: Task 02 will take a long time to run. Around 10000 iterations are needed')
print('CTRL-C to stop')
pc = 0
registers = [0, 0, 0, 0, 0, 0]
#states = set()
#states.add(get_state())
halts = dict()
steps = 0
while step():
    #state = get_state()
    #if state in states:
    #    break
    #states.add(state)
    steps = steps + 1
    if pc == halt_pc:
        if registers[halt_r] in halts:
            break
        halts[registers[halt_r]] = steps
        if len(halts) % 100 == 0:
            print(len(halts))

print()
print('Task 02: {}'.format(max(halts.items(), key=lambda kv: kv[1])[0]))
