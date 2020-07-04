from collections import Counter
from itertools import chain
from typing import List, Optional, Tuple

from utils import read_input

Point = Tuple[int, int]

INPUT = read_input(6)
INPUT_TEST = """
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
""".strip().splitlines()


def day6(input_: List[str], safe_range: int = 10000) -> None:
    def parse_line(line: str) -> Point:
        a, b = line.split(', ')
        return int(a), int(b)

    points = list(map(parse_line, input_))

    def distance(a: Point, b: Point) -> int:
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    def closest(a: Point) -> Optional[Point]:
        min_dist = 100000000
        min_p = None
        for b in points:
            dist = distance(a, b)
            if dist < min_dist:
                min_dist = dist
                min_p = b
            elif min_dist == dist:
                min_p = None
        return min_p

    plane = dict((p, p) for p in points)
    (min_x, max_x), (min_y, max_y) = [(min(l), max(l)) for l in zip(*points)]

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            closest_ = closest((x, y))
            if closest_ is not None:
                plane[(x, y)] = closest_

    is_infinite = set()
    for edge_p in chain(((min_x, y) for y in range(min_y, max_y + 1)), ((max_x, y) for y in range(min_y, max_y + 1)),
                        ((x, min_y) for x in range(min_x, max_x + 1)), ((x, max_y) for x in range(min_x, max_x + 1))):
        if edge_p in plane:
            is_infinite.add(plane[edge_p])

    for k, v in Counter(plane.values()).most_common():
        if k in is_infinite:
            continue

        print(v)
        break

    def in_safe_region(a: Point) -> bool:
        return sum(distance(a, b) for b in points) < safe_range

    safe_plane = {}
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            safe_plane[(x, y)] = in_safe_region((x, y))

    print(sum(safe_plane.values()))


day6(INPUT_TEST, 32)
day6(INPUT)
