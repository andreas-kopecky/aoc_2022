from dataclasses import field, dataclass
from itertools import cycle
from typing import Callable, Iterator


# @@@@
def bar(top: int) -> set[tuple[int, int]]:
    return {(2, top + 4), (3, top + 4), (4, top + 4), (5, top + 4)}

#  @
# @@@
#  @
def cross(top: int) -> set[tuple[int, int]]:
    return {(3, top + 6), (2, top + 5), (3, top + 5), (4, top + 5), (3, top + 4)}

#   @
#   @
# @@@
def inverse_l(top: int) -> set[tuple[int, int]]:
    return {(4, top + 6), (4, top + 5), (2, top + 4), (3, top + 4), (4, top + 4)}

# @
# @
# @
# @
def straight_i(top: int) -> set[tuple[int, int]]:
    return{(2, top + 7), (2, top + 6), (2, top + 5), (2, top + 4)}

# @@
# @@
def cube(top: int) -> set[tuple[int, int]]:
    return  {(2, top + 5), (3, top + 5),  (2, top + 4), (3, top + 4),}


@dataclass
class Chamber:
    sequence: list[Callable[[int], set[tuple[int, int]]]]
    jets: str
    width: int = 7
    chamber: set = field(default_factory=set)
    moves: tuple[str] = field(init=False)
    top: int = field(default=0, init=False)
    rock_sequence: Iterator = field(init=False)
    move_sequence: Iterator = field(init=False)

    def __post_init__(self):
        self.moves = tuple(map({"<": "left", ">": "right"}.__getitem__, self.jets))
        self.chamber.clear()
        self.chamber.update((col, 0) for col in range(self.width))
        self.rock_sequence = cycle(enumerate(self.sequence))
        self.move_sequence = cycle(enumerate(self.moves))

    def play(self, n_rocks: int) -> int:
        tracking = {}
        for i in range(n_rocks):
            rock_idx, rock_func = next(self.rock_sequence)
            rock = rock_func(self.top)
            while True:
                move_idx, direction = next(self.move_sequence)
                if i > 1000:
                    key = (rock_idx, move_idx)
                    if key in tracking:
                        previous_i, elevation = tracking[key]
                        period = i - previous_i
                        if i % period == n_rocks % period:
                            cycle_height = self.top - elevation
                            rocks_remaining = n_rocks - i
                            cycles_remaining = (rocks_remaining // period) + 1
                            return elevation + (cycle_height * cycles_remaining)
                    else:
                        tracking[key] = (i, self.top)

                rock = getattr(self, direction)(rock)
                new_position = self.down(rock)
                if new_position == rock:
                    self.chamber.update(rock)
                    self.top = max(coordinate[1] for coordinate in self.chamber)
                    break
                rock = new_position

        return self.top

    def left(self, rock: set[tuple[int, int]]) -> set[tuple[int, int]]:
        new_rock = {(col - 1, row) for col, row in rock}
        if any(coord[0] < 0 for coord in new_rock) or new_rock & self.chamber:
            return rock
        return new_rock

    def right(self, rock: set[tuple[int, int]]) -> set[tuple[int, int]]:
        new_rock = {(col + 1, row) for col, row in rock}
        if any(coord[0] >= self.width for coord in new_rock) or new_rock & self.chamber:
            return rock
        return new_rock

    def down(self, rock: set[tuple[int, int]]) -> set[tuple[int, int]]:
        new_rock = {(col, row - 1) for col, row in rock}
        return rock if new_rock & self.chamber else new_rock


def solve() -> tuple[int, int]:
    with open("../data/17_input.txt", "r") as fh:
        jets = fh.read().strip()

    sequence = [bar, cross, inverse_l, straight_i, cube]
    chamber = Chamber(sequence, jets)
    part_1 = chamber.play(2022)

    chamber = Chamber(sequence, jets)
    part_2 = chamber.play(1_000_000_000_000)
    return part_1, part_2


if __name__ == "__main__":
    print(solve())