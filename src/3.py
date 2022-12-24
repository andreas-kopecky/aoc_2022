from string import ascii_lowercase, ascii_uppercase
from itertools import chain, islice

values = {c: i + 1 for i, c in enumerate(chain(ascii_lowercase, ascii_uppercase))}

def matching(left: str, right: str) -> int:
    return values[set(left).intersection(set(right)).pop()]


def badge(first: str, second: str, third: str) -> int:
    return values[(set(first) & set(second) & set(third)) .pop()]


def solve():
    items = []
    with open("../data/3_input.txt", "r") as fh:
        for s in fh:
            s = s.strip()
            items.append((s[:len(s)//2], s[len(s)//2:]))

    result_1 = sum(map(lambda t: matching(*t), items))

    with open("../data/3_input.txt") as fh:
        lines = []
        for s in fh:
            lines.append(s.strip())

    result_2 = 0
    for i in range(0, len(lines), 3):
        rucksacks = lines[i:i+3]
        result_2 += badge(*rucksacks)

    return result_1, result_2

if __name__ == "__main__":
    print(solve())


def solve() -> Tuple[int, int]:
    # your code here!
    return result_part1, result_part_2
