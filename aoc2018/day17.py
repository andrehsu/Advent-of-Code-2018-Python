import re
from collections import defaultdict, deque
from itertools import count
from typing import List, Tuple

from utils import read_input, test_case

INPUT = read_input(17)
INPUT_TEST = test_case('''
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
''')

Pos = Tuple[int, int]


def day17(input_: List[str]) -> None:
    min_y = 99999999
    max_y = -1
    min_x = 99999999
    max_x = -1

    ground = defaultdict(lambda: defaultdict(lambda: '.'))
    for line in input_:
        at, start, end = map(int, re.findall(r'\d+', line))
        if line[0] == 'x':
            xs = [at]
            ys = range(start, end + 1)
        else:
            xs = range(start, end + 1)
            ys = [at]

        min_x = min(min_x, *xs)
        max_x = max(max_x, *xs)
        min_y = min(min_y, *ys)
        max_y = max(max_y, *ys)

        for x in xs:
            for y in ys:
                ground[y][x] = '#'
    min_x -= 1
    max_x += 1
    heads = deque([(min_y, 500)])

    def visualize():
        with open('visualize.txt', 'w+') as f:
            for i in range(1, max_y + 1):
                for j in range(min_x, max_x + 1):
                    f.write(ground[i][j])
                f.write('\n')

    def bounds(i: int, j: int) -> Tuple[int, int]:
        start = 999999
        end = 0
        for step in (-1, 1):
            for k in count(j, step):
                if ground[i][k] == '#' or k > max_x or k < min_x:
                    break
                start = min(start, k)
                end = max(end, k)
        return start, end + 1

    def can_settle(i: int, j: int) -> bool:
        start, end = bounds(i, j)
        for j in range(start, end):
            if ground[i + 1][j] == '.':
                return False
        return True

    while heads:
        (i, j) = heads.popleft()
        ground[i][j] = '|'

        if ground[i + 1][j] not in ('#', '~'):  # if there is space to drop, drop
            if i != max_y:  # if not at bottom of map
                heads.append((i + 1, j))
        else:
            if can_settle(i, j):  # if the water can settle
                start, end = bounds(i, j)
                for k in range(start, end):  # convert | to ~
                    ground[i][k] = '~'
                if (i - 1, j) not in heads:  # weird optimization that somehow works
                    heads.append((i - 1, j))
            else:  # spill over
                for step in (-1, 1):
                    for k in count(j, step):
                        if ground[i][k] == '#':  # if hit a wall, stop expanding
                            break
                        elif ground[i + 1][k] == '.':  # if space, stop dropping from there
                            heads.append((i, k))
                            break
                        elif ground[i + 1][k] == '|':  # if already traversed, don't traverse
                            break
                        else:  # else expand
                            ground[i][k] = '|'

    visualize()  # write visualization to file for debug
    print(len([i for row in ground.values() for i in row.values() if i in ('~', '|')]))  # count all water tiles
    print(len([i for row in ground.values() for i in row.values() if i == '~']))  # count stationary water tiles


day17(INPUT_TEST)
day17(INPUT)
