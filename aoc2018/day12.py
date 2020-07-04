from collections import defaultdict
from typing import Dict, List, Tuple

from utils import read_input, test_case

INPUT = read_input(12)
TEST_INPUT = test_case('''
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
''')


def iterate(rules: Dict[str, str], pots: Dict[int, str]) -> Dict[int, str]:
    i_min = min(pots)
    i_max = max(pots)

    pots_new: Dict[int, str] = defaultdict(lambda: '.')
    for i in range(i_min - 1, i_max + 1 + 1):
        key = ''.join(pots[j] for j in range(i - 2, i + 2 + 1))
        value = rules[key]
        pots_new[i] = value

    return pots_new


def parse_input(input_: List[str]) -> Tuple[Dict[int, str], Dict[str, str]]:
    pots: Dict[int, str] = defaultdict(lambda: '.')
    for i, e in enumerate(input_[0].split(': ')[1]):
        pots[i] = e

    rules: Dict[str, str] = defaultdict(lambda: '.')
    for line in input_[2:]:
        a, b = line.split(' => ')
        rules[a] = b

    return pots, rules


def score(pots: Dict[int, str]) -> int:
    return sum(k for k, v in pots.items() if v == '#')


def part1(input_: List[str]) -> int:
    pots, rules = parse_input(input_)

    for _ in range(20):
        pots = iterate(rules, pots)

    return score(pots)


def part2(input_: List[str]) -> int:
    pots, rules = parse_input(input_)

    for _ in range(100):
        pots = iterate(rules, pots)

    sum_ = score(pots)
    next_score = score(iterate(rules, pots))
    sum_ += (next_score - sum_) * (50000000000 - 100)

    return sum_


def day12(input_: List[str]):
    print(part1(input_))
    print(part2(input_))


day12(INPUT)
