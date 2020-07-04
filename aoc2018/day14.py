from utils import read_input

INPUT = int(read_input(14)[0])


def part1(input_: int) -> str:
    board = [3, 7]

    elf_i = 0
    elf_j = 1

    for _ in range(input_):
        recipe_i = board[elf_i]
        recipe_j = board[elf_j]
        recipe_new = recipe_i + recipe_j
        board.extend(map(int, str(recipe_new)))

        elf_i = (elf_i + 1 + recipe_i) % len(board)
        elf_j = (elf_j + 1 + recipe_j) % len(board)

    out = []
    for i in range(input_, input_ + 10):
        out.append(board[i])

    return ''.join(map(str, out))


def part2(input_: int) -> int:
    digits = list(map(int, str(input_)))
    board = [3, 7]
    elf_i = 0
    elf_j = 1

    while True:
        recipe_i = int(board[elf_i])
        recipe_j = int(board[elf_j])
        recipe_new = recipe_i + recipe_j
        for d in map(int, str(recipe_new)):
            board.append(d)
            if board[-len(digits):] == digits:
                return len(board) - len(digits)

        elf_i = (elf_i + 1 + recipe_i) % len(board)
        elf_j = (elf_j + 1 + recipe_j) % len(board)


def day14(input_: int) -> None:
    print(part1(input_))
    print(part2(input_))


print(part2(59414))
day14(INPUT)
