from collections import defaultdict
from dataclasses import dataclass
from typing import List, Set, Dict, Optional

from utils import read_input, test_case

INPUT = read_input(7)
INPUT_TEST = test_case('''
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
''')

Graph = Dict[str, Set[str]]


def parse_graph(input_: List[str]) -> Graph:
    graph = defaultdict(set)

    for line in input_:
        words = line.split()
        prereq = words[1]
        step = words[7]
        graph[step].add(prereq)
        if prereq not in graph:
            graph[prereq] = set()

    return graph


def remove_open_steps(graph: Graph) -> List[str]:
    open_steps = []
    for k, v in list(graph.items()):
        if not v:
            del graph[k]
            open_steps.append(k)

    return open_steps


def remove_prereq(graph: Graph, prereq: str) -> None:
    for prereqs in graph.values():
        if prereq in prereqs:
            prereqs.remove(prereq)


def part1(input_: List[str]) -> str:
    graph = parse_graph(input_)
    out = []

    queue = remove_open_steps(graph)
    while queue:
        queue.sort()
        step = queue.pop(0)
        out.append(step)
        remove_prereq(graph, step)

        queue.extend(remove_open_steps(graph))

    return ''.join(out)


def part2(input_: List[str],
          test_case: bool = False) -> int:
    def time(step: str):
        time = ord(step) - ord('A') + 1
        if not test_case:
            time += 60
        return time

    @dataclass
    class Worker:
        step: str = ''
        time: Optional[int] = None

        @property
        def active(self) -> bool:
            return self.time is not None

    worker_count = 2 if test_case else 5
    workers = [Worker() for _ in range(worker_count)]

    graph = parse_graph(input_)
    out = []

    seconds = 0
    queue = remove_open_steps(graph)
    while queue or any(worker.active for worker in workers):
        for worker in workers:
            if not queue:
                break

            if not worker.active:
                step = queue.pop(0)
                worker.step = step
                worker.time = time(step)

        for worker in workers:
            if worker.active:
                worker.time -= 1

        for worker in workers:
            if worker.time == 0:
                out.append(worker.step)
                worker.time = None
                remove_prereq(graph, worker.step)

        queue.extend(remove_open_steps(graph))
        queue.sort()

        seconds += 1

    return seconds


def day7(input_: List[str]) -> None:
    print(part1(input_))
    print(part2(input_))


print(part1(INPUT_TEST))
print(part2(INPUT_TEST, True))
day7(INPUT)
