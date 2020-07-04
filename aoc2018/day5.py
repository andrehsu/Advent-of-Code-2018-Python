from string import ascii_lowercase

from utils import read_input

INPUT = read_input(5)[0]
INPUT_TEST = 'dabAcCaCBAcCcaDA'


def part5(polymer: str) -> None:
    def collapsed(polymer: str) -> str:
        len_old = 0
        len_new = len(polymer)
        while len_old != len_new:
            len_old = len_new

            for c in ascii_lowercase:
                polymer = polymer.replace(c + c.upper(), '').replace(
                    c.upper() + c, '')

            len_new = len(polymer)
        return polymer

    print(len(collapsed(polymer)))

    print(
        min(
            len(collapsed(polymer.replace(c, '').replace(c.upper(), '')))
            for c in ascii_lowercase))


part5(INPUT_TEST)
part5(INPUT)
