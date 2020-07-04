from typing import Dict, List, Tuple

from utils import read_input, test_case

Loc = Tuple[int, int]

INPUT = read_input(13)


class Cart:
    def __init__(self, tracks: List[List[str]], s: str, i: int, j: int):
        self._i = i
        self._j = j
        self._tracks = tracks
        if s == '^':
            self.d = 0
        elif s == '>':
            self.d = 1
        elif s == 'v':
            self.d = 2
        elif s == '<':
            self.d = 3
        self.next_turn = -1

    def _turn_left(self) -> None:
        self.d = (self.d + 3) % 4

    def _turn_right(self) -> None:
        self.d = (self.d + 1) % 4

    def move(self) -> None:
        if self.d == 0:
            self._i -= 1
        elif self.d == 1:
            self._j += 1
        elif self.d == 2:
            self._i += 1
        elif self.d == 3:
            self._j -= 1

        next_track = self._tracks[self._i][self._j]
        if next_track == '\\':
            if self.d in (1, 3):
                self._turn_right()
            else:
                self._turn_left()
        elif next_track == '/':
            if self.d in (1, 3):
                self._turn_left()
            else:
                self._turn_right()
        elif next_track == '+':
            if self.next_turn == -1:
                self._turn_left()
                self.next_turn = 0
            elif self.next_turn == 0:
                self.next_turn = 1
            elif self.next_turn == 1:
                self._turn_right()
                self.next_turn = -1

    def get_loc(self) -> Tuple[int, int]:
        return self._i, self._j


def build_tracks(input_: List[str]) -> Tuple[List[List[str]], Dict[Loc, Cart]]:
    carts = {}
    tracks = []
    for i, line in enumerate(input_):
        row: List[str] = []
        tracks.append(row)
        for j, e in enumerate(line):
            if e in ('<', '>'):
                carts[(i, j)] = Cart(tracks, e, i, j)
                e = '-'
            elif e in ('v', '^'):
                carts[(i, j)] = Cart(tracks, e, i, j)
                e = '|'
            row.append(e)
    return tracks, carts


def part1(input_: List[str]) -> None:
    tracks, carts = build_tracks(input_)

    while True:
        new_carts: Dict[Tuple[int, int], Cart] = {}
        for i, row in enumerate(tracks):
            for j in range(len(row)):
                if (i, j) in carts:
                    cart = carts.pop((i, j))
                    cart.move()
                    new_loc = cart.get_loc()
                    if new_loc in new_carts or new_loc in carts:
                        i, j = new_loc
                        print(f'{j},{i}')
                        return
                    new_carts[new_loc] = cart
        carts = new_carts


def part2(input_: List[str]) -> None:
    tracks, carts = build_tracks(input_)

    while True:
        new_carts: Dict[Loc, Cart] = {}
        for i, row in enumerate(tracks):
            for j in range(len(row)):
                if (i, j) in carts:
                    cart = carts.pop((i, j))
                    cart.move()
                    new_loc = cart.get_loc()
                    alive = True
                    if new_loc in new_carts:
                        del new_carts[new_loc]
                        alive = False
                    if new_loc in carts:
                        del carts[new_loc]
                        alive = False
                    if alive:
                        new_carts[new_loc] = cart
        carts = new_carts
        if len(carts) == 1:
            i, j = next(iter(carts.values())).get_loc()
            print(f'{j},{i}')
            return


def day13(input_):
    part1(input_)
    part2(input_)


TEST_INPUT = test_case(R'''
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
''')

part1(TEST_INPUT)

TEST_INPUT = test_case(R'''
/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
''')
part2(TEST_INPUT)

day13(INPUT)
