from itertools import accumulate, cycle

from utils import read_input

INPUT = read_input(1)


def day1(input_):
    changes = list(map(int, input_))

    print(sum(changes))
    seen = {0}
    print(
        next(
            i for i in accumulate(cycle(changes)) if i in seen or seen.add(i)))


day1(INPUT)
