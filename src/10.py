from textwrap import wrap

import numpy as np

from operator import add
from functools import reduce


def get_delta(command: str) -> list[int]:
    if command == "noop":
        return [0]
    _, value = command.split()
    return [0, int(value)]

def solve() -> tuple[int, str]:
    with open("../data/10_input.txt", "r") as fh:
        commands = [line.strip() for line in fh]

    # Part 1
    deltas = reduce(add, [get_delta(command) for command in commands])
    register = np.cumsum([1] + deltas)
    strength = np.dot(register[19::40], np.ogrid[20:240:40])

    # Part 2
    sprite_idx = np.arange(1, 241) % 40
    crt_overlay = sprite_idx - register[:-1]
    pixel = ((crt_overlay >= 0) & (crt_overlay < 3))
    output = "".join(["#" if i else '.' for i in pixel])

    return strength, "\n".join(r for r in wrap(output, width=40))

if __name__ == "__main__":
    signal, crt = solve()
    print(signal)
    print(crt)