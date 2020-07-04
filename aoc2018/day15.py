from day15_lib import day15
from utils import read_input, test_case

INPUT = read_input(15)

INPUT_TEST = test_case("""
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""")

INPUT_TEST_1 = test_case('''
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
''')

INPUT_TEST_2 = test_case('''
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
''')

INPUT_TEST_3 = test_case('''
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
''')

INPUT_TEST_4 = test_case('''
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
''')

INPUT_TEST_5 = test_case('''
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
''')

# with debugger:
#     assert part1(INPUT_TEST) == 27730
# assert part1(INPUT_TEST_1) == 36334
# assert part1(INPUT_TEST_2) == 39514
# assert part1(INPUT_TEST_3) == 27755
# assert part1(INPUT_TEST_4) == 28944
# assert part1(INPUT_TEST_5) == 18740
day15(INPUT)
