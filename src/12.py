import numpy as np
from scipy.sparse import dok_array
from scipy.sparse.csgraph import dijkstra


def solve() -> tuple[int, int]:
    with open("../data/12_input.txt", "r") as fh:
        content = np.fromstring(fh.read(), dtype=np.uint8)

    mountain = content.reshape((-1, 137))[:, :-1]

    # Save starting positions for later, redefine them with correct height
    start, end = (np.nonzero(mountain == ord(loc)) for loc in ("S", "E"))
    mountain[start] = ord("a")
    mountain[end] = ord("z")

    # Build graph template
    G = dok_array((mountain.size, mountain.size), dtype=np.uint8)
    V = np.arange(mountain.size).reshape(mountain.shape)

    left  = V[ :  ,  :-1].flatten()
    right = V[ :  , 1:  ].flatten()
    upper = V[ :-1,  :  ].flatten()
    lower = V[1:  ,  :  ].flatten()

    # Fill graph with connections under given conditions (delta height < 2)
    for direction_one, direction_two in [(left, right), (right, left), (upper, lower), (lower, upper)]:
        linked = mountain.flat[direction_one] + 1 >= mountain.flat[direction_two]
        G[(direction_one[linked], direction_two[linked])] = 1

    # Find shortest paths
    D = dijkstra(G, indices=np.ravel_multi_index(start, dims=mountain.shape), min_only=True)
    part_1 = int(D[np.ravel_multi_index(end, dims=mountain.shape)])

    start_2 = np.nonzero(mountain == ord("a"))
    D = dijkstra(G, indices=np.ravel_multi_index(start_2, dims=mountain.shape), min_only=True)
    part_2 = int(D[np.ravel_multi_index(end, dims=mountain.shape)])
    return part_1, part_2


if __name__ == "__main__":
    print(solve())