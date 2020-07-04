from collections import defaultdict
from typing import DefaultDict, List

from utils import read_input

INPUT = read_input(4)

INPUT_TEST = """
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
""".strip().splitlines()


def day4(input_: List) -> None:
    input_.sort()

    schedule: DefaultDict[int, DefaultDict[int, int]] = defaultdict(
        lambda: defaultdict(int))
    guard: int = -1
    for line in input_:
        words = line.split()
        minute = int(words[1][3:5])
        if words[2] == 'falls':
            start = minute
        elif words[2] == 'wakes':
            end = minute
            # noinspection PyUnboundLocalVariable
            for j in range(start, end):
                schedule[guard][j] += 1
        else:
            guard = int(words[3][1:])

    guard = max(schedule, key=lambda k: sum(schedule[k].values()))
    minute = max(schedule[guard], key=lambda k: schedule[guard][k])

    print(guard * minute)

    guard = max(schedule, key=lambda k: max(schedule[k].values()))
    minute = max(schedule[guard], key=lambda k: schedule[guard][k])

    print(guard * minute)


day4(INPUT_TEST)
day4(INPUT)
