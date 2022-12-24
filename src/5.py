from __future__ import annotations

import re

from collections import deque
from typing import Tuple, List, Dict

pattern = re.compile(r"^\[([A-Z])\]\s$")
move_pattern = re.compile(r"^move ([0-9]+) from ([0-9]+) to ([0-9]+)\s$")

def load_stack(line: str) -> List:
    stack = []
    for i in range(0, len(line), 4):
        m = pattern.match(line[i:i+4])
        stack.append(None if m is None else m.groups()[0])
    return stack


def parse_command(line: str) -> Tuple[int, int, int]:
    return tuple(map(int, move_pattern.match(line).groups()))


class Stacks:
    def __init__(self, stacks: Dict):
        self._stacks: Dict = stacks

    def move_n(self, n: int, src: int, dst: int):
        for i in range(n):
            self._stacks[dst].appendleft(self._stacks[src].popleft())

    def move_n_blocked(self, n: int, src: int, dst: int):
        crates = reversed([self._stacks[src].popleft() for _ in range(n)])
        for crate in crates:
            self._stacks[dst].appendleft(crate)

    @property
    def state(self) -> str:
        return "".join([d[0] for d in self._stacks.values()])


    @classmethod
    def create_stacks(cls, setup: List[str]) -> Stacks:
        _stacks = {}
        for i, members in enumerate(zip(*list(map(load_stack, setup)))):
            _stacks[i + 1] = deque([m for m in members if m is not None])
        return cls(stacks=_stacks)


def solve() -> Tuple[str, str]:
    with open("../data/5_input.txt") as fh:
        content = fh.readlines()

    setup = content[:8]
    moves = content[10:]

    stacks = Stacks.create_stacks(setup)
    for move in moves:
        stacks.move_n(*parse_command(move))
    result_1 = stacks.state

    stacks = Stacks.create_stacks(setup)
    for move in moves:
        stacks.move_n_blocked(*parse_command(move))
    result_2 = stacks.state

    return result_1, result_2

if __name__ == "__main__":
    print(solve())



