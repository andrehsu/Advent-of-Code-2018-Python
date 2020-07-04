import re
from itertools import count
from typing import List

from utils import read_input, test_case

INPUT = read_input(10)
TEST_INPUT = test_case('''
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
''')


def day10(input_: List[str]):
    stars = []
    for line in input_:
        px, py, vx, vy = map(int, re.findall(r'-?\d+', line))
        stars.append((px, py, vx, vy))

    min_width = 10000000000000000000000

    for i in count():
        new_stars = []
        for px, py, vx, vy in stars:
            px += vx
            py += vy
            new_stars.append((px, py, vx, vy))

        max_y = max(k[1] for k in new_stars)
        min_y = min(k[1] for k in new_stars)
        width = max_y - min_y

        if width < min_width:
            min_width = width
        if width > min_width:
            max_x = max(k[0] for k in stars)
            min_x = min(k[0] for k in stars)
            max_y = max(k[1] for k in stars)
            min_y = min(k[1] for k in stars)
            star_map = set((px, py) for px, py, *_ in stars)
            for y in range(min_y, max_y + 1):
                row = []
                for x in range(min_x, max_x + 1):
                    if (x, y) in star_map:
                        row.append('#')
                    else:
                        row.append(' ')
                print(''.join(row))
            print(i)
            break

        stars = new_stars


day10(TEST_INPUT)
day10(INPUT)
