#!/usr/bin/env pipenv-run
from tqdm import tqdm

r0 = 0
r1 = 0
r2 = 0
r3 = 0
r4 = 0
r5 = 0

last_halt = None
halts = set()
# This varies from input to input
# But then again, other inputs does not translate to this code
halts_needed = 10295

r3 = 0
r4 = r3 | 65536
r3 = 2176960
with tqdm(total=halts_needed + 1) as pbar:
    while True:
        r1 = r4 & 255
        r3 = r3 + r1
        r3 = r3 & 16777215
        r3 = r3 * 65899
        r3 = r3 & 16777215
        r1 = int(256 > r4)
        if r1:
            # ==== BEGIN not program logic ===
            pbar.update(1)
            if last_halt is None:
                # First halt
                print('Task 01: {}'.format(r3))
            if r3 in halts:
                # r3 have started to loop around
                print('Task 02: {}'.format(last_halt))
                print('Results found after {} halts'.format(len(halts) + 1))
                break
            last_halt = r3
            halts.add(last_halt)
            # ==== END not program logic ===

            r1 = int(r3 == r0)
            if r1:
                # Actual program halt
                print('Program halted before all results were found, try setting a random value for r0')
                break
            r4 = r3 | 65536
            r3 = 2176960
            continue
        r1 = 0
        while True:
            r5 = r1 + 1
            r5 = r5 * 256
            r5 = int(r5 > r4)
            if r5:
                r4 = r1
                break
            r1 = r1 + 1
