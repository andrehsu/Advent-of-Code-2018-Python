import re
from collections import defaultdict
from typing import Callable, Dict, Set, Tuple

Op = Callable[[int, int, int], None]
with open('inputs/day16.txt') as f:
    INPUT = f.read()

INPUT_PART1, INPUT_PART2 = INPUT.split('\n\n\n\n')

registers = [0, 0, 0, 0]


def addr(a, b, c):
    registers[c] = registers[a] + registers[b]


def addi(a, b, c):
    registers[c] = registers[a] + b


def mulr(a, b, c):
    registers[c] = registers[a] * registers[b]


def muli(a, b, c):
    registers[c] = registers[a] * b


def banr(a, b, c):
    registers[c] = registers[a] & registers[b]


def bani(a, b, c):
    registers[c] = registers[a] & b


def borr(a, b, c):
    registers[c] = registers[a] | registers[b]


def bori(a, b, c):
    registers[c] = registers[a] | b


def setr(a, _, c):
    registers[c] = registers[a]


def seti(a, _, c):
    registers[c] = a


def gtir(a, b, c):
    registers[c] = 1 if a > registers[b] else 0


def gtri(a, b, c):
    registers[c] = 1 if registers[a] > b else 0


def gtrr(a, b, c):
    registers[c] = 1 if registers[a] > registers[b] else 0


def eqir(a, b, c):
    registers[c] = 1 if a == registers[b] else 0


def eqri(a, b, c):
    registers[c] = 1 if registers[a] == b else 0


def eqrr(a, b, c):
    registers[c] = 1 if registers[a] == registers[b] else 0


ops_all = {
    addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri,
    gtrr, eqir, eqri, eqrr
}

count = 0

op_opcode_map: Dict[int, Set[Op]] = defaultdict(lambda: set(ops_all))


def extract_ints(s: str) -> Tuple[int, ...]:
    return tuple(map(int, re.findall(r'\d+', s)))


for group in INPUT_PART1.split('\n\n'):
    lines = group.splitlines()
    pre = extract_ints(lines[0])
    opcode, a, b, c = extract_ints(lines[1])
    post = extract_ints(lines[2])

    matches = 0
    for op in ops_all:
        registers = list(pre)
        op(a, b, c)
        if tuple(registers) == post:
            matches += 1
        else:
            ops = op_opcode_map[opcode]
            if op in ops:
                ops.remove(op)

    if matches >= 3:
        count += 1

print(count)

changed = True
while changed:
    changed = False
    for opcode, ops in op_opcode_map.items():
        if len(ops) == 1:
            op = next(iter(ops))
            for opcode_, ops_ in op_opcode_map.items():
                if opcode_ != opcode and op in ops_:
                    changed = True
                    ops_.remove(op)

registers = [0, 0, 0, 0]

for line in INPUT_PART2.splitlines():
    opcode, a, b, c = extract_ints(line)
    op_func = next(iter(op_opcode_map[opcode]))
    op_func(a, b, c)

print(registers[0])
