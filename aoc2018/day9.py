import re
from collections import defaultdict, deque
from itertools import count
from typing import Dict

from utils import read_input

TEST_INPUT = '30 players; last marble is worth 5807 points'
INPUT = read_input(9)[0]


def day9(input_: str):
    players_num, last_value = map(int, re.findall(r'\d+', input_))
    players: Dict[int, int] = defaultdict(int)

    circle = deque([0])

    player_i = 0

    for i in count(1):
        if i % 23 == 0:
            players[player_i] += i
            for _ in range(7):
                circle.appendleft(circle.pop())
            players[player_i] += circle.popleft()
        else:
            circle.append(circle.popleft())
            circle.append(circle.popleft())

            circle.appendleft(i)

        player_i = (player_i + 1) % players_num

        if i == last_value:
            print(max(players.values()))
        elif i == last_value * 100:
            print(max(players.values()))
            break


day9(TEST_INPUT)
day9(INPUT)
