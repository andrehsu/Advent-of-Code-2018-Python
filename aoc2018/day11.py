import numba
import numpy as np

from utils import read_input

INPUT = int(read_input(11)[0])
TEST_INPUT = 18


@numba.njit
def day11_numba(input_):
    grid = np.zeros((301, 301), np.int32)
    for x in range(1, 301):
        for y in range(1, 301):
            rack_id = x + 10
            power = rack_id * y
            power += input_
            power *= rack_id
            power = power // 100 % 10
            power -= 5
            grid[x, y] = power

    sum_table = np.zeros((302, 302), np.int32)
    for x in range(300, 0, -1):
        for y in range(300, 0, -1):
            sum_table[x, y] = grid[x, y] + sum_table[x + 1, y] + sum_table[x, y + 1] - sum_table[x + 1, y + 1]
    max_sum = -1
    p1_coord = (-1, -1)
    for x in range(1, 301 - 3):
        for y in range(1, 301 - 3):
            sum_ = sum_table[x, y] - sum_table[x + 3, y] - sum_table[x, y + 3] + sum_table[x + 3, y + 3]
            if sum_ > max_sum:
                p1_coord = x, y
                max_sum = sum_

    max_sum = -1
    p2_coord = (-1, -1, -1)
    for s in range(1, 301):
        for x in range(1, 301 - s):
            for y in range(1, 301 - s):
                sum_ = sum_table[x, y] - sum_table[x + s, y] - sum_table[x, y + s] + sum_table[x + s, y + s]
                if sum_ > max_sum:
                    p2_coord = x, y, s
                    max_sum = sum_

    return p1_coord, p2_coord


def day11(input_: int):
    p1_coord, p2_coord = day11_numba(input_)
    x, y = p1_coord
    print(f'{x},{y}')
    x, y, s = p2_coord
    print(f'{x},{y},{s}')


day11(TEST_INPUT)
day11(INPUT)
