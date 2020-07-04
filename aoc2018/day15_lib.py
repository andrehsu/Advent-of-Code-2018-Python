from types import TracebackType
from typing import Tuple, List, Set, Dict, Optional, NamedTuple, Type, Callable

debug_mode = False

Coordinate = Tuple[int, int]


class Debugger:
    def __enter__(self) -> None:
        global debug_mode
        self.debug_mode_initial = debug_mode
        debug_mode = True

    def __exit__(self, exc_type: Type, exc_val: Exception, exc_tb: TracebackType) -> None:
        global debug_mode
        debug_mode = self.debug_mode_initial


debugger = Debugger()


def debug_print(value: Callable[[], str]) -> None:
    if debug_mode:
        print(value())


def adjacent_coords(coord: Coordinate) -> List[Coordinate]:
    i, j = coord
    return [(i - 1, j), (i, j - 1), (i, j + 1), (i + 1, j)]


class BfsNode(NamedTuple):
    first_move: Coordinate
    coord: Coordinate

    def create_child(self, coord) -> 'BfsNode':
        return BfsNode(self.first_move, coord)


class Space:
    @staticmethod
    def coord_key(space: 'Space') -> Coordinate:
        return space.coord

    def __init__(self, ctx: 'Simulator', coord: Coordinate):
        self.ctx = ctx
        self.coord = coord

    def adjacents(self) -> List['Space']:
        cavern = self.ctx.cavern

        return [cavern[coord] for coord in adjacent_coords(self.coord) if coord in cavern]


class Empty(Space):
    pass


class Wall(Space):
    pass


class BfsResult(NamedTuple):
    start: Coordinate
    dist: int
    target: Coordinate


class Unit(Space):
    class NoEnemyError(Exception):
        pass

    @staticmethod
    def hp_key(unit: 'Unit') -> int:
        return unit.hp

    def __init__(self, ctx: 'Simulator', coord: Coordinate, hp: int, ap: int):
        super().__init__(ctx, coord)
        self.hp = hp
        self.ap = ap

    def do_turn(self) -> None:
        cavern = self.ctx.cavern

        all_enemies = [other for other in cavern.values() if isinstance(other, Unit) and self.is_enemy_of(other)]
        if not all_enemies:
            raise Unit.NoEnemyError()

        target_coords = {space.coord for enemy in all_enemies for space in enemy.adjacents()}

        if self.coord not in target_coords:
            next_move = self.bfs_move(target_coords)
            if next_move is not None:
                cavern[self.coord] = Empty(self.ctx, self.coord)
                cavern[next_move] = self
                self.coord = next_move

        self.attack_adj_enemies()

    def bfs_move(self, target_coords: Set[Coordinate]) -> Optional['Coordinate']:
        for space in self.adjacents():
            if space.coord in target_coords and isinstance(space, Empty):
                return space.coord

        cavern = self.ctx.cavern

        moves = 2
        open_set: List[BfsNode] = list()
        for first_move in self.adjacents():
            if isinstance(first_move, Empty):
                for adj in first_move.adjacents():
                    if isinstance(adj, Empty) and not any(node.coord == adj.coord for node in open_set):
                        open_set.append(BfsNode(first_move.coord, adj.coord))

        closed_set: Set[Coordinate] = set()
        for node in open_set:
            closed_set.add(node.first_move)
            closed_set.add(node.coord)

        target_reached = False
        while not target_reached and open_set:
            next_open_set: List[BfsNode] = []
            for node in open_set:
                if node.coord in target_coords:
                    target_reached = True
                    break

                for adj in cavern[node.coord].adjacents():
                    if isinstance(adj, Empty) and adj.coord not in closed_set:
                        closed_set.add(adj.coord)
                        next_open_set.append(node.create_child(adj.coord))
            else:
                moves += 1
                open_set = next_open_set

        if target_reached:
            open_set = [node for node in open_set if node.coord in target_coords]
            open_set.sort(key=lambda x: x.first_move)
            open_set.sort(key=lambda x: x.coord)
            return open_set[0].first_move

        return None

    def attack_adj_enemies(self) -> None:
        cavern = self.ctx.cavern

        adj_enemies: List[Unit] = [adj for adj in self.adjacents() if isinstance(adj, Unit) and self.is_enemy_of(adj)]

        if adj_enemies:
            # noinspection PyTypeChecker
            adj_enemies.sort(key=Space.coord_key)
            adj_enemies.sort(key=Unit.hp_key)

            other = adj_enemies[0]

            other.hp -= self.ap
            if other.hp <= 0:
                cavern[other.coord] = Empty(self.ctx, other.coord)

    def is_enemy_of(self, other: 'Unit') -> bool:
        return type(self) is not type(other)


class Elf(Unit):
    pass


class Goblin(Unit):
    pass


class Simulator:
    def __init__(self, input_: List[str], *, elf_attack_power: int = 3):
        def parse_input_to_cavern() -> Tuple[Dict[Coordinate, Space], int, int]:
            max_i = max_j = 0
            cavern = {}
            for i, row in enumerate(input_):
                max_i = max(max_i, i)
                for j, char in enumerate(row):
                    max_j = max(max_j, j)
                    # noinspection PyUnusedLocal
                    e: Space
                    if char == '#':
                        e = Wall(self, (i, j))
                    elif char == '.':
                        e = Empty(self, (i, j))
                    elif char == 'E':
                        e = Elf(self, (i, j), 200, elf_attack_power)
                    elif char == 'G':
                        e = Goblin(self, (i, j), 200, 3)
                    else:
                        raise ValueError(f'Unrecognized input character: {char}')
                    cavern[e.coord] = e
            return cavern, max_i, max_j

        self.cavern, self.max_i, self.max_j = parse_input_to_cavern()
        self.ran = False
        self._outcome = 0
        self._all_elves_alive = False

    @property
    def all_elf_alive(self) -> bool:
        if not self.ran:
            raise ValueError('Not yet ran')
        return self._all_elves_alive

    @property
    def outcome(self) -> int:
        if not self.ran:
            raise ValueError('Not yet ran')
        return self._outcome

    def run(self) -> None:
        if self.ran:
            return
        else:
            self.ran = True

        elf_count = 0
        for space in self.cavern.values():
            if isinstance(space, Elf):
                elf_count += 1

        rounds = 0
        battle_done = False
        while not battle_done:
            did_turn: Set[Coordinate] = set()
            debug_print(lambda: f'After {rounds} rounds:')
            debug_print(lambda: self.cavern_repr())
            for space in self.cavern.values():
                if isinstance(space, Unit) and space.coord not in did_turn:
                    try:
                        space.do_turn()
                        did_turn.add(space.coord)
                    except Unit.NoEnemyError:
                        battle_done = True
                        break
            else:
                rounds += 1

        debug_print(lambda: self.cavern_repr())

        hp_sum = sum(space.hp for space in self.cavern.values() if isinstance(space, Unit))
        self._outcome = hp_sum * rounds

        for space in self.cavern.values():
            if isinstance(space, Elf):
                elf_count -= 1

        self._all_elves_alive = elf_count == 0

    def cavern_repr(self) -> str:
        sb = []
        for i in range(self.max_i + 1):
            for j in range(self.max_j + 1):
                space = self.cavern[(i, j)]
                if isinstance(space, Wall):
                    sb.append('#')
                elif isinstance(space, Empty):
                    sb.append('.')
                elif isinstance(space, Elf):
                    sb.append('E')
                elif isinstance(space, Goblin):
                    sb.append('G')
                else:
                    raise ValueError(f'Unexpected space type: {type(space)}')
            sb.append('\n')
        return ''.join(sb)


def part1(input_: List[str]) -> int:
    simulator = Simulator(input_)
    simulator.run()

    return simulator.outcome


def part2(input_: List[str]) -> int:
    for ap in range(4, 1000):
        simulator = Simulator(input_, elf_attack_power=ap)
        simulator.run()
        if simulator.all_elf_alive:
            return simulator.outcome

    raise ValueError('A.P. larger than 999')


def day15(input_: List[str]) -> None:
    print(part1(input_))
    print(part2(input_))
