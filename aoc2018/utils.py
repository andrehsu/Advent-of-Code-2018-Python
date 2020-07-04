from typing import List

_inputs_dir = 'inputs'


def read_input(day: int, ) -> List[str]:
    dir_ = f'{_inputs_dir}/day{day}.txt'
    with open(dir_) as f:
        lines = f.read().splitlines()

    return lines


def test_case(text: str) -> List[str]:
    return text.strip('\n').splitlines()
