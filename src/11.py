from __future__ import annotations

import re

from collections import deque
from dataclasses import dataclass, field
from functools import reduce
from math import lcm
from operator import mul, add
from typing import Callable

pattern = re.compile(
r"""Monkey (?P<identifier>\d+):
\s*Starting items: (?P<items>[\d, ]*)
\s*Operation: new = old (?P<op>[+*]) (?P<arg>\d+|old)
\s*Test: divisible by (?P<divisor>\d+)
\s*If true: throw to monkey (?P<true_target>\d+)
\s*If false: throw to monkey (?P<false_target>\d+)""",
flags=re.MULTILINE)

@dataclass
class Monkey:
    identifier: int
    items: deque[int]
    op: Callable[[int], int]
    divisor: int
    targets: dict[bool, int] = field(default_factory=dict)
    inspections: int = field(default=0, init=False)

    def play(self, relief: int, factor: int | None = None) -> list[tuple[int, int]]:
        targets = []
        while self.items:
            worry, target = self.toss(relief)
            if factor:
                worry %= factor
            targets.append((worry, target))
        return targets

    def toss(self, relief: int) -> tuple[int, int]:
        item = self.items.popleft()
        worry = self.op(item) // relief
        target = self.targets[worry % self.divisor == 0]
        self.inspections += 1
        return worry, target

    def catch(self, worry: int):
        self.items.append(worry)

    @classmethod
    def from_str(cls, definition: str) -> Monkey:
        content = pattern.match(definition).groupdict()
        params = {"identifier": int(content["identifier"]), "items": deque(map(int, content["items"].split(", ")))}

        operator = mul if content["op"] == "*" else add
        if content["arg"] == "old":
            params["op"] = lambda worry: operator(worry, worry)
        else:
            right = int(content["arg"])
            params["op"] = lambda worry: operator(worry, right)
        params["divisor"] = int(content["divisor"])
        params["targets"] = {True: int(content["true_target"]), False: int(content["false_target"])}
        return cls(**params)


def play(monkeys: list[Monkey], rounds: int, relief: int):
    if relief == 1:
        factor =  lcm(*(monkey.divisor for monkey in monkeys))
    else:
        factor = None
    for i in range(rounds):
        for monkey in monkeys:
            targets = monkey.play(relief, factor)
            for worry, target in targets:
                monkeys[target].catch(worry)


def solve() -> tuple[int, int]:
    with open("../data/11_input.txt", "r") as fh:
        definitions = fh.read().split("\n\n")

    monkeys = list(map(Monkey.from_str, definitions))
    play(monkeys, 20, relief=3)
    inspections = sorted(m.inspections for m in monkeys)
    part_1 = reduce(mul, inspections[-2:])

    monkeys = list(map(Monkey.from_str, definitions))
    play(monkeys, 10000, relief=1)
    inspections = sorted(m.inspections for m in monkeys)
    part_2 = reduce(mul, inspections[-2:])
    return part_1, part_2

if __name__ == '__main__':
    print(solve())


