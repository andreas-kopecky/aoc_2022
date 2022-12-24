from operator import eq, gt, iconcat

from dataclasses import dataclass
from functools import total_ordering, singledispatch, reduce
from typing import Callable, Any


@dataclass
class ComparableBase:
    value: int

def make_op(op) -> Callable[[Any, Any], bool]:
    def _op(self, other):
        match other:
            case self.__class__(value):
                return op(self.value, value)
            case list():
                return op([self], other)
    return _op

Comparable = total_ordering(type("Comparable", (ComparableBase,), dict(__eq__=make_op(eq), __gt__=make_op(gt))))

@singledispatch
def make_comparable(value):
    pass

@make_comparable.register(int)
def _(value) -> Comparable:
    return Comparable(value)

@make_comparable.register(list)
def _(value) -> list[Comparable]:
    return list(map(make_comparable, value))


def solve() -> tuple[int, int]:
    with open("../data/13_input.txt", "r") as fh:
        lines = [list(map(eval, line.split("\n"))) for line in fh.read().strip().split("\n\n")]


    comparable_lines = [[make_comparable(left), make_comparable(right)] for left, right in lines]
    part_1 = sum(i for i, (left, right) in enumerate(comparable_lines, start=1) if left < right )


    flattened_once = list(reduce(iconcat, comparable_lines, []))
    flattened_once.extend([[[Comparable(2)]], [[Comparable(6)]]])
    flattened_once.sort()

    a = flattened_once.index([[Comparable(2)]]) + 1
    b = flattened_once.index([[Comparable(6)]]) + 1

    return part_1, a * b

if __name__ == "__main__":
    print(solve())