from typing import Tuple, List


def full_cover(l_l: int, l_u: int, r_l: int, r_u: int) -> bool:
    return (l_l <= r_l <= r_u <= l_u) or (r_l <= l_l <= l_u <= r_u)


def cover(l_l: int, l_u: int, r_l: int, r_u: int) -> bool:
    return (l_l <= r_l <= l_u) or (r_l <= l_l <= r_u)


def solve() -> Tuple[int, int]:
    with open("../data/4_input.txt") as fh:
        ranges: List[Tuple[int, int, int, int]] = [tuple(map(int, line.replace("-", ",").split(","))) for line in fh]

    return sum(map(lambda c: full_cover(*c), ranges)),  sum(map(lambda c: cover(*c), ranges))


if __name__ == "__main__":
    print(solve())