from typing import Iterable, Iterator, List

from utils import read_input

INPUT = read_input(8)[0]
INPUT_TEST = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'


class Node:

    def __init__(self, children: List['Node'], metadata: List[int]):
        self.children = children
        self.metadata = metadata

    @classmethod
    def from_config(cls, config: Iterable[int]) -> 'Node':
        config = iter(config)
        return cls.__from_config(config)

    @classmethod
    def __from_config(cls, config: Iterator[int]) -> 'Node':
        children_len = next(config)
        metadata_len = next(config)

        children = []
        for _ in range(children_len):
            child = Node.__from_config(config)
            children.append(child)

        metadata = []
        for _ in range(metadata_len):
            metadata.append(next(config))

        node = cls(children, metadata)

        return node

    @property
    def value(self):
        if self.children:
            value = 0
            for i in self.metadata:
                i -= 1
                if 0 <= i < len(self.children):
                    value += self.children[i].value
        else:
            value = sum(self.metadata)

        return value

    @property
    def all_metadata_sum(self):
        return sum(self.metadata) + sum(
            child.all_metadata_sum for child in self.children)


def day8(input_: str):
    root = Node.from_config(map(int, input_.split()))

    print(root.all_metadata_sum)

    print(root.value)


day8(INPUT_TEST)
day8(INPUT)
