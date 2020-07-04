import re
from collections import defaultdict

from utils import read_input

INPUT = read_input(3)


def day3(input_):
    def parse_claim(line: str):
        return tuple(map(int, re.findall(r'\d+', line)))

    claims = list(map(parse_claim, input_))
    fabric = defaultdict(list)

    for id_, dx, dy, x, y in claims:
        for i in range(dx, dx + x):
            for j in range(dy, dy + y):
                fabric[(i, j)].append(id_)

    print(len([i for i in fabric.values() if len(i) > 1]))

    ids_all = set(map(lambda x: x[0], claims))
    ids_overlapped = set(id_ for ids in fabric.values() if len(ids) > 1
                         for id_ in ids)

    print(ids_all - ids_overlapped)


day3(INPUT)
