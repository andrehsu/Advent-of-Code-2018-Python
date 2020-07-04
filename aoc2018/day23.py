import dataclasses
import re
import timeit
from typing import List

import numpy as np

from utils import read_input, test_case

INPUT = read_input(23)
INPUT_TEST_P1 = test_case('''
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
''')
INPUT_TEST_P2 = test_case('''
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
''')


@dataclasses.dataclass(frozen=True)
class Nanobot:
    x: int
    y: int
    z: int
    r: int

    def dist(self, other: 'Nanobot') -> int:
        return abs(self.x - other.x) + \
               abs(self.y - other.y) + \
               abs(self.z - other.z)

    def in_range(self, other: 'Nanobot') -> bool:
        return other.dist(self) <= self.r

    @property
    def pos(self):
        return self.x, self.y, self.z


def part1(input_: List[str]) -> int:
    nanobots = parse_nanobots(input_)

    nanobot_max = max(nanobots, key=lambda x: x.r)

    count = 0
    for nanobot in nanobots:
        if nanobot_max.in_range(nanobot):
            count += 1

    return count


def part2(input_: List[str]) -> int:
    nanobots = parse_nanobots(input_)

    xs, ys, zs = zip(map(lambda n: (n.x, n.y, n.z), nanobots))

    x_min = min(xs)
    x_max = max(xs)
    y_min = min(ys)
    y_max = max(ys)
    z_min = min(zs)
    z_max = max(zs)

    def sft_pos(x, y, z):
        return x - x_min, y - y_min, z - z_min

    space = np.zeros((x_max - x_min, y_max - y_min, z_max - z_min))

    for nanobot in nanobots:
        x, y, z, r = dataclasses.astuple(nanobot)


def parse_nanobots(input_: List[str]) -> List[Nanobot]:
    nanobots = []
    for row in input_:
        x, y, z, r = map(int, re.findall(r'-?\d+', row))
        nanobots.append(Nanobot(x, y, z, r))

    return nanobots


# print(part1(INPUT_TEST_P1))
print(timeit.timeit(r'print(part2(INPUT_TEST_P2))', number=1, globals=globals()))
print(part2(INPUT_TEST_P2))

# print(part1(INPUT))
# print(part2(INPUT))
