from collections import Counter
from itertools import combinations
from typing import List

from utils import read_input

INPUT = read_input(2)


def day2(input_: List[str]) -> None:
    count_2 = 0
    count_3 = 0

    for id_ in input_:
        c = Counter(id_)
        if 2 in c.values():
            count_2 += 1
        if 3 in c.values():
            count_3 += 1

    print(count_2 * count_3)

    for a, b in combinations(input_, 2):
        count_diff = sum(i != j for i, j in zip(a, b))
        if count_diff == 1:
            print(''.join(i for i, j in zip(a, b) if i == j))


day2(INPUT)
