import copy
from collections import Counter
from typing import List

from utils import read_input, test_case

INPUT_TEST = test_case('''
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
''')

INPUT = read_input(18)

Plot = List[List[str]]


def print_plot(plot: Plot):
    for row in plot:
        for i in row:
            print(i, end='')
        print()


def resource_value(plot: Plot) -> int:
    trees = 0
    yards = 0
    for row in plot:
        for i in row:
            if i == '|':
                trees += 1
            elif i == '#':
                yards += 1
    return trees * yards


def next_plot(plot: Plot) -> Plot:
    new_plot = copy.deepcopy(plot)
    for i, row in enumerate(plot):
        for j in range(len(row)):
            prev = plot[i][j]

            yards = 0
            trees = 0
            for k in range(i - 1, i + 2):
                for l in range(j - 1, j + 2):
                    if not (i == k and j == l) and 0 <= k < len(plot) and 0 <= l < len(row):
                        adj = plot[k][l]
                        if adj == '|':
                            trees += 1
                        elif adj == '#':
                            yards += 1
            new = prev
            if prev == '.' and trees >= 3:
                new = '|'
            elif prev == '|' and yards >= 3:
                new = '#'
            elif prev == '#' and not (yards >= 1 and trees >= 1):
                new = '.'

            new_plot[i][j] = new

    return new_plot


def part1(plot: Plot):
    for _ in range(10):
        plot = next_plot(plot)

    print(resource_value(plot))


def part2(plot: Plot):
    rvs = []
    seen = {}
    cycles = Counter()

    for minute in range(1_000_000_000):
        rv = resource_value(plot)
        if rv in seen:
            last_minute = seen[rv]
            cycles[minute - last_minute] += 1

            if cycles.most_common(1)[0][1] == 5:
                cycle = cycles.most_common(1)[0][0]
                print(rvs[-(cycle - (1_000_000_000 - minute) % cycle)])
                break

        rvs.append(rv)
        seen[rv] = minute

        plot = next_plot(plot)


def day18(input_: List[str]):
    plot = list(map(list, input_))
    part1(plot)
    part2(plot)


# day18(INPUT_TEST)
day18(INPUT)
